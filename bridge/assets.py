"""Deterministic, bounded authoritative PNG crops. No client image transport."""
import hashlib
import math
import warnings
import struct
import zlib
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from .validation import Failure, require, asset_key

MAX_BYTES = 32 * 1024 * 1024
MAX_PIXELS = 40_000_000
MAX_ASSETS = 32
MAX_SET_BYTES = 64 * 1024 * 1024


def png(data):
    require(0 < len(data) <= MAX_BYTES, 'ASSET_LIMIT_EXCEEDED', 422)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            image = Image.open(BytesIO(data))
            require(image.format == 'PNG' and not getattr(image, 'is_animated', False), 'SOURCE_PNG_INVALID', 409)
            require(0 < image.width * image.height <= MAX_PIXELS, 'ASSET_LIMIT_EXCEEDED', 422)
            image.load()
            return image
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombWarning, Image.DecompressionBombError):
        raise Failure('SOURCE_PNG_INVALID', 409) from None


def verify_crop(data, artifact):
    require(len(data) == artifact['byte_size'] and hashlib.sha256(data).hexdigest() == artifact['sha256'], 'PERSISTENCE_UNVERIFIED', 503)
    image = png(data)
    require(image.size == (artifact['width'], artifact['height']), 'PERSISTENCE_UNVERIFIED', 503)


def prepare_assets(page, manifest, storage, source_bucket, output_bucket):
    assets = [a for i in page['items'] for a in i.get('assets', [])]
    require(len(assets) <= MAX_ASSETS, 'ASSET_LIMIT_EXCEEDED', 422)
    require(output_bucket == 'page-ingest', 'CONFIGURATION_MISSING', 503)
    source = next(i for i in manifest['page_images'] if i['page_no'] == page['publication']['page_no'])
    raw = storage.download_bounded(source_bucket, source['path'], MAX_BYTES)
    require(hashlib.sha256(raw).hexdigest() == source['sha256'], 'SOURCE_PNG_HASH_MISMATCH', 409)
    image = png(raw)
    require(image.size == (source['width_px'], source['height_px']), 'SOURCE_PNG_DIMENSIONS_MISMATCH', 409)
    prepared = []; total = 0
    for a in assets:
        anchor = a['page_anchor']
        require(anchor['source_page_image_sha256'] == source['sha256'], 'SOURCE_PNG_HASH_MISMATCH', 409)
        x0,y0,x1,y1 = anchor['bbox_norm']; w,h = image.size
        bounds = [math.floor(x0*w), math.floor(y0*h), math.ceil(x1*w), math.ceil(y1*h)]
        require(anchor['bbox_px'] is None or anchor['bbox_px'] == bounds, 'ASSET_BBOX_MISMATCH', 409)
        crop = image.crop(bounds).convert('RGBA')
        data = canonical_png(crop)
        total += len(data)
        require(len(data) <= MAX_BYTES and total <= MAX_SET_BYTES, 'ASSET_LIMIT_EXCEEDED', 422)
        artifact = {'bucket':output_bucket, 'key':asset_key(page,a['asset_id']),
                    'media_type':'image/png', 'sha256':hashlib.sha256(data).hexdigest(),
                    'byte_size':len(data), 'width':crop.width, 'height':crop.height}
        require(a['artifact'] is None or a['artifact'] == artifact, 'ASSET_ARTIFACT_MISMATCH', 409)
        a['artifact'] = artifact
        anchor['bbox_px'] = bounds
        prepared.append((a,data))
    return prepared


def canonical_png(image):
    """RGBA8, filter 0, stored DEFLATE blocks: independent of zlib encoder version."""
    w,h = image.size; pixels = image.tobytes(); stride = w*4
    scan = b''.join(b'\0'+pixels[y*stride:(y+1)*stride] for y in range(h))
    blocks=[]
    for start in range(0,len(scan),65535):
        block=scan[start:start+65535]; size=len(block)
        blocks.append(bytes([int(start+size == len(scan))])+struct.pack('<HH',size,size^65535)+block)
    compressed=b'\x78\x01'+b''.join(blocks)+struct.pack('>I',zlib.adler32(scan)&0xffffffff)
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',compressed)+chunk(b'IEND',b'')
