import spidev
import time
import os

IMG_DIR = 'images'

# SX1262 SPI setup
SPI_BUS = 0
SPI_DEVICE = 0
SPI_MAX_SPEED_HZ = 5000000

def initialise_spi():
    spi = spidev.SpiDev()
    spi.open(SPI_BUS, SPI_DEVICE)
    spi.max_speed_hz = SPI_MAX_SPEED_HZ
    return spi

def send_packet(spi, packet):
    spi.xfer2(packet)

def transmit_image(spi, filename):
    with open(filename, 'rb') as f:
        chunk_size = 240  # LoRa packet size limit
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            send_packet(spi, list(chunk))
            time.sleep(1)  # Add delay between packets to ensure proper transmission

def main():
    spi = initialise_spi()

    while True:
        command = input("Enter 'send' to send the latest image, 'exit' to exit: ").strip().lower()
        if command == 'send':
            # Get the latest image file
            image_files = sorted([f for f in os.listdir(IMG_DIR) if f.endswith('.png')], reverse=True)
            if not image_files:
                print("No images to send.")
                continue
            
            latest_image = os.path.join(IMG_DIR, image_files[0])
            print(f"Transmitting {latest_image}")
            transmit_image(spi, latest_image)
            print("Image transmission complete.")
        elif command == 'exit':
            break

if __name__ == '__main__':
    main()
