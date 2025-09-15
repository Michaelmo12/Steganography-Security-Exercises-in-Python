import struct

class BMP24:
    @staticmethod
    def _read_headers(data: bytes):
        if data[:2] != b'BM':
            raise ValueError("Not BMP")
        pixel_offset = struct.unpack_from("<I", data, 10)[0]
        width = struct.unpack_from("<i", data, 18)[0]
        height = struct.unpack_from("<i", data, 22)[0]
        bpp = struct.unpack_from("<H", data, 28)[0]
        if bpp != 24:
            raise ValueError("Only 24bpp BMP supported")
        return pixel_offset, width, height

    @staticmethod
    def _row_stride(width: int):
        row_bytes = width * 3
        return row_bytes + (4 - (row_bytes % 4)) % 4

    @staticmethod
    def embed_text(input_bmp, output_bmp, text):
        with open(input_bmp, "rb") as f:
            data = bytearray(f.read())
        pixel_offset, width, height = BMP24._read_headers(data)
        stride = BMP24._row_stride(width)

        payload = text.encode()
        bitlen = len(payload) * 8
        header_bits = struct.pack("<I", bitlen)
        full = header_bits + payload

        bits = []
        for b in full:
            for i in range(8):
                bits.append((b >> i) & 1)

        h_abs = abs(height)
        capacity = width * h_abs * 3
        if len(bits) > capacity:
            raise ValueError("Message too large")

        bi = 0
        for row in range(h_abs):
            row_in_file = (h_abs - 1 - row) if height > 0 else row
            offset = pixel_offset + row_in_file * stride
            for col in range(width):
                pix = offset + col * 3
                for c in range(3):
                    if bi >= len(bits):
                        break
                    data[pix + c] = (data[pix + c] & 0xFE) | bits[bi]
                    bi += 1
                if bi >= len(bits):
                    break
            if bi >= len(bits):
                break

        with open(output_bmp, "wb") as f:
            f.write(data)

    @staticmethod
    def extract_text(bmp_path):
        with open(bmp_path, "rb") as f:
            data = f.read()
        pixel_offset, width, height = BMP24._read_headers(data)
        stride = BMP24._row_stride(width)
        h_abs = abs(height)

        def read_bits(n):
            out = []
            bi = 0
            for row in range(h_abs):
                row_in_file = (h_abs - 1 - row) if height > 0 else row
                offset = pixel_offset + row_in_file * stride
                for col in range(width):
                    pix = offset + col * 3
                    for c in range(3):
                        out.append(data[pix + c] & 1)
                        bi += 1
                        if bi >= n:
                            return out
            return out

        header_bits = read_bits(32)
        bitlen = sum((bit << i) for i, bit in enumerate(header_bits))
        payload_bits = read_bits(32 + bitlen)[32:]
        byts = bytearray()
        for i in range(0, len(payload_bits), 8):
            b = 0
            for j in range(8):
                if i + j < len(payload_bits):
                    b |= (payload_bits[i + j] << j)
            byts.append(b)
        return byts.decode(errors="replace")
