import cv2
import numpy as np
from numba import cuda
import time

# CUDA kernel
@cuda.jit
def apply_median_filter_cuda(input_channel, output, kernel_size):
    x, y = cuda.grid(2)
    edge = kernel_size // 2
    if x >= edge and y >= edge and x < input_channel.shape[1] - edge and y < input_channel.shape[0] - edge:
        neighbors = []
        for dy in range(-edge, edge + 1):
            for dx in range(-edge, edge + 1):
                neighbors.append(input_channel[y + dy, x + dx])
        neighbors.sort()
        output[y, x] = neighbors[len(neighbors) // 2]

def apply_median_filter(input_channel, kernel_size):
    # Convert input to device array
    input_channel_device = cuda.to_device(input_channel)
    output_device = cuda.device_array(input_channel.shape, dtype=np.uint8)

    # Define grid and block dimensions
    threadsperblock = (16, 16)
    blockspergrid_x = int(np.ceil(input_channel.shape[1] / threadsperblock[1]))
    blockspergrid_y = int(np.ceil(input_channel.shape[0] / threadsperblock[0]))
    blockspergrid = (blockspergrid_x, blockspergrid_y)

    # Launch kernel
    apply_median_filter_cuda[blockspergrid, threadsperblock](input_channel_device, output_device, kernel_size)
    
    # Copy the result back to host
    return output_device.copy_to_host()

def main():
    # Read the image
    image = cv2.imread('../resources/sp_img_gray_noise_heavy.png', cv2.IMREAD_COLOR)

    # Split the image into its color channels
    channels = cv2.split(image)

    start_time = time.time()

    # Apply median filter to each channel
    filtered_channels = [apply_median_filter(ch, 5) for ch in channels]  # Kernel size is 5

    end_time = time.time()
    print(f"Filtering time: {end_time - start_time} seconds")

    # Merge the channels back
    filtered_image = cv2.merge(filtered_channels)

    # Save the images before and after filtering
    cv2.imwrite('before.jpg', image)
    cv2.imwrite('after.jpg', filtered_image)

if __name__ == "__main__":
    main()