from deproto import Protobuf

# Example protobuf string from Google Maps
pb_string = (
    "!3m1!1e3!4m12!3m11!1s0x4795cd1c65280cb9:0xad3b34d7340adc02"
    "!5m3!1s2024-12-21!4m1!1i2!8m2!3d49.167174!4d7.22149!9m1!1b1"
    "!16s%2Fg%2F1tfr93pp"
)


def main():
    # Create decoder instance
    decoder = Protobuf(pb_string)

    # Decode the string into a tree structure
    cluster = decoder.decode()

    print("Original Tree Structure:")
    print("-----------------------")
    decoder.print_tree()

    # Make changes to values
    cluster[4][3][5][1].change("2025-01-01")

    print("\nModified Tree Structure:")
    print("-----------------------")
    decoder.print_tree()

    # Encode back to protobuf format
    encoded = decoder.encode()
    print("\nEncoded String:")
    print("--------------")
    print(encoded)


if __name__ == "__main__":
    main()
