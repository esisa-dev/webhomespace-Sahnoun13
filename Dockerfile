FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN pip3 install Flask


# Create a new user with a password
RUN useradd -m -p $(openssl passwd -6 1234) dev
RUN useradd -m -p $(openssl passwd -6 12345) dev1

# Set the permissions of the /home/dev directory to 755 (readable by everyone)
RUN chmod -R 755 /home/dev

# Set the working directory to /app and copy the Flask app into the container
WORKDIR /app
COPY . .
RUN chmod -R 777 /app

# USER dev

# Create files and directories
RUN echo "This is file 1." > /home/dev/file1.txt
RUN echo "This is file 2." > /home/dev/file2.txt
RUN mkdir /home/dev/folder1
RUN echo "This is file 3." > /home/dev/folder1/file3.txt
RUN echo "This is file 4." > /home/dev/folder1/file4.txt
RUN mkdir /home/dev/folder2
RUN echo "This is file 5." > /home/dev/folder2/file5.txt
RUN echo "This is file 6." > /home/dev/folder2/file6.txt
RUN mkdir /home/dev/folder3
RUN echo "This is file 7." > /home/dev/folder3/file7.txt
RUN echo "This is file 8." > /home/dev/folder3/file8.txt
RUN mkdir /home/dev/folder4
RUN echo "This is file 9." > /home/dev/folder4/file9.txt
RUN echo "This is file 10." > /home/dev/folder4/file10.txt
RUN mkdir /home/dev/folder5
RUN echo "This is file 11." > /home/dev/folder5/file11.txt
RUN echo "This is file 12." > /home/dev/folder5/file12.txt
RUN mkdir /home/dev/folder6
RUN echo "This is file 13." > /home/dev/folder6/file13.txt
RUN echo "This is file 14." > /home/dev/folder6/file14.txt
RUN mkdir /home/dev/folder7
RUN echo "This is file 15." > /home/dev/folder7/file15.txt

RUN mkdir /home/dev/folder1/folder
RUN echo "This is file 16." > /home/dev/folder1/folder/file16.txt
RUN echo "This is file 17." > /home/dev/folder1/folder/file17.txt


# USER dev1

# Start the Flask app
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]