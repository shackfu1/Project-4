for i in range(10):
    AddrsData = open("tcp_addrs_" + str(i) + ".txt","r").read()
    AddrsData = AddrsData.split()
    SourceAddrs = AddrsData[0]
    DestAddrs = AddrsData[1]
    ByteString = bytes([])
    for Byte in SourceAddrs.split("."):
        ByteString += (int(Byte).to_bytes())
    for Byte in DestAddrs.split("."):
        ByteString += (int(Byte).to_bytes())
    ByteString += (int("0").to_bytes())
    ByteString += (int("6").to_bytes())
    with open("tcp_data_" + str(i) + ".dat", "rb") as fp:
        TcpData = fp.read()
        TcpLen = len(TcpData).to_bytes(2)
        ByteString += (TcpLen)
        TcpChecksum = int.from_bytes(TcpData[16:18])
        TcpZeroChcksum = TcpData[:16] + b'\x00\x00' + TcpData[18:]
        if len(TcpZeroChcksum) % 2 == 1:
            TcpZeroChcksum += b'\x00'

        data = ByteString + TcpZeroChcksum
        offset = 0  # byte offset into data
        total = 0
        while offset < len(data):
            # Slice 2 bytes out and get their value:
            word = int.from_bytes(data[offset:offset + 2], "big")
            total += word
            total = (total & 0xffff) + (total >> 16)
            offset += 2  # Go to the next 2-byte value

        checksum = (~total) & 0xffff
        if checksum == TcpChecksum:
            print("PASS")
        else:
            print("FAIL")