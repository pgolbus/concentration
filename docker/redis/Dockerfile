# Use the official Redis image as the base
FROM redis:latest

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the Redis configuration file into the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose the Redis default port (6379)
EXPOSE 6379

# Start the Redis server using the specified configuration file
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
