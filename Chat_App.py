#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from socket import AF_INET, socket, SOCK_STREAM, SOCK_DGRAM
from threading import Thread


class Chat_App(Frame):

    def __init__(self, parent):  # Starting frame
        Frame.__init__(self, parent)
        self.parent = parent
        self.BigFrame = Frame(parent)  # Our big frame
        self.BigFrame.grid()
        self.Frame = Frame(self.BigFrame)  # Our first frame to show connection screen
        self.Frame.grid()
        self.Frame2 = Frame(self.BigFrame)  # Our second frame to show chat window
        self.Frame2.grid()
        self.GUI()  # Start GUI

    def GUI(self):  # Inside GUI
        self.label1 = Label(self.Frame, bg="#E8E6E3", height=20, width=85)
        self.label1.grid(row=1, column=1, rowspan=17, columnspan=50)
        self.label2 = Label(self.Frame, fg="Black", bg="#E8E6E3", text="Project 1", font="Helvetica 16 bold")
        self.label2.grid(row=2, column=22, rowspan=2, columnspan=10)
        self.label3 = Label(self.Frame, fg="Black", bg="#E8E6E3", text="Enter Destination IP:", font="Helvetica 10")
        self.label3.grid(row=5, column=1, rowspan=2, columnspan=13)
        self.entry1 = Entry(self.Frame, width=30)  # Destination ip entry widget
        self.entry1.grid(row=5, column=18, rowspan=2, columnspan=12)
        self.label4 = Label(self.Frame, fg="Black", bg="#E8E6E3", text="Protocol:", font="Helvetica 10")
        self.label4.grid(row=7, column=5, rowspan=1, columnspan=5)
        self.protocol = IntVar()  # For determining protocols
        self.radiobutton1 = Radiobutton(self.Frame, fg="Black", bg="#E8E6E3", text="TCP", variable=self.protocol,
                                        value=int(1))  # TCP Connection
        self.radiobutton1.grid(row=7, column=22)
        self.radiobutton2 = Radiobutton(self.Frame, fg="Black", bg="#E8E6E3", text="UDP", variable=self.protocol,
                                        value=int(2))  # UDP Connection
        self.radiobutton2.grid(row=7, column=30)
        self.button1 = Button(self.Frame, fg="Black", bg="#E8E6E3", text="Start Connection =>", width=20,
                              command=self.start_connection)  # Used to start connection
        self.button1.grid(row=9, column=16, rowspan=2, columnspan=15)
        self.label5 = Label(self.Frame, fg="Red", bg="#E8E6E3", text="", font="Helvetica 10")
        self.label5.grid(row=11, column=15, rowspan=2, columnspan=17)

    def start_connection(self):  # When user press on start connection button
        self.label5.config(text="Waiting to Connection Partner")  # Change text in order to inform user
        self.Frame.grid_forget()  # Delete previous connection screen
        self.parent.title("Pychat Host")  # New screen title
        self.parent.geometry("400x500")  # New screen size
        self.label6 = Label(self.Frame2, bg="#706563", height=33, width=57)
        self.label6.grid(row=1, column=1, rowspan=42, columnspan=39)
        self.text1 = Text(self.Frame2, height=22, width=41)  # Chat History
        self.text1.grid(row=2, column=2, rowspan=31, columnspan=36)
        self.scrollbar1 = Scrollbar(self.Frame2, orient=VERTICAL, command=self.text1.yview)  # Scrollbar for chat history
        self.scrollbar1.grid(row=2, column=37, rowspan=31, columnspan=1, sticky="NS")
        self.text1["yscrollcommand"] = self.scrollbar1.set
        self.text2 = Text(self.Frame2, height=5, width=27)  # Chat Bar for user input
        self.text2.grid(row=35, column=2, rowspan=6, columnspan=26)
        self.button3 = Button(self.Frame2, text=u"\U0001F601", height=5, width=7, command=self.emojis)  # Emoji tab
        self.button3.grid(row=35, column=35, rowspan=6, columnspan=5)
        if self.protocol.get() == 1:  # TCP Protocol
            if len(self.entry1.get()) == 0:  # If user acts as server (ie. gives no input to server ip entry)
                self.button2 = Button(self.Frame2, text="SEND", height=5, width=10, font="BOLD", command=self.TCP_Send_Message_Server)  # Button to send message
                self.button2.grid(row=35, column=26, rowspan=6, columnspan=8)
                self.ip_adress = ""  # IP Adress
                self.port = 52173  # Port Adress
                self.buffersize = 8192  # Buffer Size
                self.adress = (self.ip_adress, self.port)  # Complete adress with ip and port combined for connection
                self.connection_socket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
                self.connection_socket.bind(self.adress)  # Ready to send and receive data
                self.connection_socket.listen(1)  # Accepting connection
                self.client, self.client_address = self.connection_socket.accept()  # Accept client connection
                receive_thread = Thread(target=self.TCP_Receive_Message_Server)  # Assign Thread
                receive_thread.start()  # Start thread
                print('Connected by', self.client_address)  # For Debugging

            else:  # If user acts as client (ie. gives input to server ip entry)
                self.button2 = Button(self.Frame2, text="SEND", height=5, width=10, font="BOLD", command=self.TCP_Send_Message)  # Button to send message
                self.button2.grid(row=35, column=26, rowspan=6, columnspan=8)
                self.ip_adress = self.entry1.get()  # Get ip adress from entry widget
                self.port = 52173  # Port adress
                self.buffersize = 8192  # Buffer Size
                self.adress = (self.ip_adress, self.port)  # Complete adress with ip and port combined for connection
                self.connection_socket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
                self.connection_socket.connect(self.adress)  # Connect to server using socket
                receive_thread = Thread(target=self.TCP_Receive_Message)  # Assign Thread
                receive_thread.start()  # Start thread
        elif self.protocol.get() == 2:  # UDP Protocol
            if len(self.entry1.get()) == 0:  # If user acts as server (ie. gives no input to server ip entry)
                self.button2 = Button(self.Frame2, text="SEND", height=5, width=10, font="BOLD",
                                      command=self.UDP_Send_Message_Server)  # Button to send message
                self.button2.grid(row=35, column=26, rowspan=6, columnspan=8)
                self.ip_adress = ""  # IP Adress
                self.port = 52173  # Port Adress
                self.buffersize = 8192  # Buffer Size
                self.adress = (self.ip_adress, self.port)  # Complete adress with ip and port combined for connection
                self.connection_socket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
                self.connection_socket.bind(self.adress)  # Ready to send and receive data
                self.data, self.client_address = self.connection_socket.recvfrom(self.buffersize)
                receive_thread = Thread(target=self.UDP_Receive_Message_Server)  # Assign Thread
                receive_thread.start()  # Start thread

            else:  # If user acts as client (ie. gives input to server ip entry)
                self.button2 = Button(self.Frame2, text="SEND", height=5, width=10, font="BOLD",
                                      command=self.UDP_Send_Message)  # Button to send message
                self.button2.grid(row=35, column=26, rowspan=6, columnspan=8)
                self.ip_adress = self.entry1.get()  # Get ip adress from entry widget
                self.port = 52173  # Port adress
                self.buffersize = 8192  # Buffer Size
                self.adress = (self.ip_adress, self.port)  # Complete adress with ip and port combined for connection
                self.connection_socket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
                self.connection_socket.connect(self.adress)  # Connect to server using socket
                receive_thread = Thread(target=self.UDP_Receive_Message)  # Assign Thread
                receive_thread.start()  # Start thread
        else:
            print "Select a protocol"  # Warn user if protocol is not selected
            print self.protocol.get()  # For Debugging

    def emojis(self):  # Open emojis as popup function
        emojis = Tk()  # Create new tkinter
        emojis.title("Emojis")  # Assign a title
        label1 = Label(emojis, height=1, width=31)
        label1.grid(row=0, column=0, rowspan=7, columnspan=22)
        button1 = Button(emojis, text=u"\U0001F601", relief=FLAT, command=self.OnClick1)  # 1st Emoji
        button1.grid(row=0, column=0)
        button2 = Button(emojis, text=u"\U0001F602", relief=FLAT, command=self.OnClick2)  # 2st Emoji
        button2.grid(row=0, column=1)
        button3 = Button(emojis, text=u"\U0001F603", relief=FLAT, command=self.OnClick3)  # 3st Emoji
        button3.grid(row=0, column=2)
        button4 = Button(emojis, text=u"\U0001F604", relief=FLAT, command=self.OnClick4)  # 4st Emoji
        button4.grid(row=0, column=3)
        button5 = Button(emojis, text=u"\U0001F605", relief=FLAT, command=self.OnClick5)  # 5st Emoji
        button5.grid(row=0, column=4)
        button6 = Button(emojis, text=u"\U0001F609", relief=FLAT, command=self.OnClick6)  # 6st Emoji
        button6.grid(row=0, column=5)
        button7 = Button(emojis, text=u"\U0001F60A", relief=FLAT, command=self.OnClick7)  # 7st Emoji
        button7.grid(row=0, column=6)
        button8 = Button(emojis, text=u"\U0001F60D", relief=FLAT, command=self.OnClick8)  # 8st Emoji
        button8.grid(row=0, column=7)
        button9 = Button(emojis, text=u"\U0001F60F", relief=FLAT, command=self.OnClick9)  # 9st Emoji
        button9.grid(row=0, column=8)
        emojis.mainloop()  # Start emoji popup

    def OnClick1(self):  # When clicked on 1st emoji
        self.text2.insert(END, u"\U0001F601")  # Insert that emoji at end of chat bar

    def OnClick2(self):  # When clicked on 2st emoji
        self.text2.insert(END, u"\U0001F602")  # Insert that emoji at end of chat bar

    def OnClick3(self):  # When clicked on 3st emoji
        self.text2.insert(END, u"\U0001F603")  # Insert that emoji at end of chat bar

    def OnClick4(self):  # When clicked on 4st emoji
        self.text2.insert(END, u"\U0001F604")  # Insert that emoji at end of chat bar

    def OnClick5(self):  # When clicked on 5st emoji
        self.text2.insert(END, u"\U0001F605")  # Insert that emoji at end of chat bar

    def OnClick6(self):  # When clicked on 6st emoji
        self.text2.insert(END, u"\U0001F609")  # Insert that emoji at end of chat bar

    def OnClick7(self):  # When clicked on 7st emoji
        self.text2.insert(END, u"\U0001F60A")  # Insert that emoji at end of chat bar

    def OnClick8(self):  # When clicked on 8st emoji
        self.text2.insert(END, u"\U0001F60D")  # Insert that emoji at end of chat bar

    def OnClick9(self):  # When clicked on 9st emoji
        self.text2.insert(END, u"\U0001F60F")  # Insert that emoji at end of chat bar

    def TCP_Send_Message(self):
        message = self.text2.get(1.0, END)  # Get the message in chat bar (TCP)
        encoded_message = message.encode("utf-8")  # We need to encode emoji in order to send it over network
        print encoded_message  # For Debugging
        self.text1.insert(END, "You: " + message)  # Add the message to chat history after sending it
        self.text2.delete(1.0, END)  # Delete current message in chat bar after sending it
        self.connection_socket.send(bytes(encoded_message))  # Send message over network

    def TCP_Send_Message_Server(self):
        message = self.text2.get(1.0, END)  # Get the message in chat bar (TCP)
        encoded_message = message.encode("utf-8")  # We need to encode emoji in order to send it over network
        print encoded_message  # For Debugging
        self.text1.insert(END, "You: " + message)  # Add the message to chat history after sending it
        self.text2.delete(1.0, END)  # Delete current message in chat bar after sending it
        self.client.send(bytes(encoded_message))  # Send message over network

    def TCP_Receive_Message(self):  # Function to receive messages when acting as Client (TCP)
        while True:
            try:
                received_message = self.connection_socket.recv(self.buffersize).decode("utf-8")  # We received encoded
                # message and in order to read it with human eyes we need to decode it
                print received_message  # For Debugging
                self.text1.insert(END, "Partner: " + received_message)  # Add the message to chat history after receiving it
            except OSError:  # If user disconnects or closes chat window
                break

    def TCP_Receive_Message_Server(self):  # Function to receive messages when acting as Server (TCP)
        while True:
            try:
                received_message = self.client.recv(self.buffersize).decode("utf-8")  # We received encoded
                print received_message  # For Debugging
                self.text1.insert(END, "Partner: " + received_message)  # Add the message to chat history after receiving it
            except OSError:  # If user disconnects or closes chat window
                break

    def UDP_Send_Message(self):  # Get the message in chat bar (UDP)
        message = self.text2.get(1.0, END)  # Get the message in chat bar
        encoded_message = message.encode("utf-8")  # We need to encode emoji in order to send it over network
        print encoded_message  # For Debugging
        self.text1.insert(END, "You: " + message)  # Add the message to chat history after sending it
        self.text2.delete(1.0, END)  # Delete current message in chat bar after sending it
        self.connection_socket.sendto(encoded_message, self.adress)  # Send message over network

    def UDP_Send_Message_Server(self):  # Get the message in chat bar (UDP)
        message = self.text2.get(1.0, END)  # Get the message in chat bar
        encoded_message = message.encode("utf-8")  # We need to encode emoji in order to send it over network
        print encoded_message  # For Debugging
        self.text1.insert(END, "You: " + message)  # Add the message to chat history after sending it
        self.text2.delete(1.0, END)  # Delete current message in chat bar after sending it
        self.connection_socket.sendto(encoded_message, self.client_address)

    def UDP_Receive_Message(self):  # Function to receive messages when acting as Client (UDP)
        while True:
            try:
                received_message = self.connection_socket.recv(self.buffersize).decode("utf-8")  # We received encoded
                # message and in order to read it with human eyes we need to decode it
                print received_message  # For Debugging
                self.text1.insert(END, "Partner: " + received_message)  # Add the message to chat history after receiving it
            except OSError:  # If user disconnects or closes chat window
                break

    def UDP_Receive_Message_Server(self):  # Function to receive messages when acting as Server (UDP)
        while True:
            try:
                received_message = self.connection_socket.recv(self.buffersize).decode("utf-8")  # We received encoded
                print received_message  # For Debugging
                self.text1.insert(END, "Partner: " + received_message)  # Add the message to chat history after receiving it
            except OSError:  # If user disconnects or closes chat window
                break


def main():  # Basic configs like geometry and creation of Tk
    root = Tk()  # Create GUI
    root.geometry("600x300")  # Size of GUI
    root.title("tk")  # Name of GUI
    my_app = Chat_App(root)
    root.mainloop()


if __name__ == '__main__':  # Lets get engine up and running
    main()
