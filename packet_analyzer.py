from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from datetime import datetime

packet_count = 0


def get_protocol(packet):
    """Identify the transport/network protocol."""
    if packet.haslayer(TCP):
        return "TCP"
    elif packet.haslayer(UDP):
        return "UDP"
    elif packet.haslayer(ICMP):
        return "ICMP"
    else:
        return f"IP Protocol {packet[IP].proto}"


def process_packet(packet):
    """Analyze and display captured IPv4 packets."""
    global packet_count

    if not packet.haslayer(IP):
        return

    packet_count += 1

    source_ip = packet[IP].src
    destination_ip = packet[IP].dst
    protocol = get_protocol(packet)

    print("\n" + "=" * 65)
    print(f"PACKET #{packet_count}")
    print("=" * 65)

    print(f"Time            : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Source IP       : {source_ip}")
    print(f"Destination IP  : {destination_ip}")
    print(f"Protocol        : {protocol}")

    if packet.haslayer(TCP):
        print(f"Source Port     : {packet[TCP].sport}")
        print(f"Destination Port: {packet[TCP].dport}")

    elif packet.haslayer(UDP):
        print(f"Source Port     : {packet[UDP].sport}")
        print(f"Destination Port: {packet[UDP].dport}")

    if packet.haslayer(Raw):
        payload = bytes(packet[Raw].load)

        # Limit output so the terminal remains readable
        if len(payload) > 100:
            payload = payload[:100] + b"..."

        print(f"Payload         : {repr(payload)}")
    else:
        print("Payload         : No payload")

    print("=" * 65)


def main():
    print("=" * 65)
    print("              NETWORK PACKET ANALYZER")
    print("=" * 65)

    print("\nEducational and authorized network monitoring only.")
    print("Press Ctrl+C to stop capturing.\n")

    try:
        sniff(
            prn=process_packet,
            store=False
        )

    except KeyboardInterrupt:
        print("\n\nPacket capture stopped.")
        print(f"Total IPv4 packets analyzed: {packet_count}")

    except PermissionError:
        print("\nPermission denied.")
        print("Run the terminal as Administrator and try again.")

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()