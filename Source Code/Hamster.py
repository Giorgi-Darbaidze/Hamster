import os
import netmiko
import tkinter as tk
from tkinter import *
from time import sleep
import tkinter.messagebox
from paramiko.ssh_exception import SSHException

def main():
    root = Tk()
    Window_port_sec(root)
    root.mainloop()


class Window_port_sec:
    def __init__(self, root):
        self.root = root
        self.root.title("Hamster")
        self.root.geometry("600x600")
        self.frame = Frame(self.root)
        self.frame.pack()
        self.interface_port_list = []
        self.interface_des_list = []
        self.interface_list = []

        # ------Main Frame Properties------

        self.top_frame = Frame(self.root, relief=RAISED, width=600, height=300, bg="#134c95")
        self.top_frame.pack()
        self.bottom_frame = Frame(root, relief=SUNKEN, width=600, height=240, bg="#134c95")
        self.bottom_frame.pack()
        self.top_left_frame = Frame(self.top_frame, relief=SUNKEN, width=450, height=500, bg="white")
        self.top_left_frame.pack(side=LEFT)
        self.top_right_frame = Frame(self.top_frame, relief=RAISED, width=150, height=500, bg="#134c95")
        self.top_right_frame.pack()

        # ------Connect/Disconnect btns & status bars------

        self.status_bar_frame = Label(root, relief=RAISED, text="This application is in Development...", anchor=W, bg="white", fg="black", width=45, height=1)
        self.status_bar_frame.place(x=75, y=540)
        self.connect_button = Button(self.top_right_frame, width=8, text="Connect", bg="white", command = self.connect, state = NORMAL)
        self.connect_button.place(x=10, y=110)
        self.disconnect_button = Button(self.top_right_frame, width=8, text="Disconnect", bg="white", command = self.disconnect_switch , state = NORMAL)
        self.disconnect_button.place(x=82, y=110)

        # ------User & Pass Buttons------

        self.username_slot = Entry(self.top_right_frame, width = 22 )
        self.username_slot.place(x=10, y=50)
        self.username_slot.insert(0, "Type Username")
        self.password_slot = Entry(self.top_right_frame, width = 22, show="*")
        self.password_slot.place(x=10, y=80)

        def username_on_entry_click(event):
            if self.username_slot.get() == "Type Username":
                self.username_slot.delete(0, tk.END)

        def username_on_focus_out(event):
            if self.username_slot.get() == "":
                self.username_slot.insert(0, "Type Username")

        self.username_slot.bind("<FocusIn>", username_on_entry_click)
        self.username_slot.bind("<FocusOut>", username_on_focus_out)

        # ------Switch IP Slot------

        self.switch_IP_slot = Entry(self.top_right_frame)
        self.switch_IP_slot.insert(0, "Type Switch IP")
        self.switch_IP_slot.place(x=10, y=10)
        self.port_list = Listbox(self.top_left_frame, width=70, height=30)
        self.port_list.place(x=12, y=10)

        def ip_on_entry_click(event):
            if self.switch_IP_slot.get() == "Type Switch IP":
                self.switch_IP_slot.delete(0, tk.END)

        def ip_on_focus_out(event):
            if self.switch_IP_slot.get() == "":
                self.switch_IP_slot.insert(0, "Type Switch IP")

        self.switch_IP_slot.bind("<FocusIn>", ip_on_entry_click)
        self.switch_IP_slot.bind("<FocusOut>", ip_on_focus_out)

        # ------Primary Buttons------

        self.show_port_btn = Button(self.top_right_frame, text="Show disabled ports", width="15", bg="white", command = self.show_disabled_ports, state = DISABLED)
        self.enable_port_btn = Button(self.top_right_frame, text="Enable port", bg="white", width="8", command = self.enable_port, state = DISABLED)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_window)




    def port_sec(self):
        self.new_window = Toplevel(self.root)
        self.app = Window_port_sec(self.new_window)


    def on_closing_window(self):
        try:
            self.connection_setup.disconnect()
            self.root.destroy()
        except:
            self.root.destroy()


    def disconnect_switch(self):
        try:
            self.connection_setup.disconnect()
            for i in range(0, len(self.interface_list)):
                self.interface_list.pop(0)
                self.port_list.delete(0)
            self.port_list.clipboard_clear()
            self.port_list.update()
            self.username_slot["state"] = NORMAL
            self.password_slot["state"] = NORMAL
            self.switch_IP_slot["state"] = NORMAL
            self.connect_button["state"] = NORMAL
            self.show_port_btn.place(x=500, y=500)
            self.enable_port_btn.place(x=500, y=500)
            self.username_slot.delete(0, 'end')
            self.password_slot.delete(0, 'end')
            self.status_bar_frame['bg'] = 'red'
            self.status_bar_frame["fg"] = "black"
            self.status_bar_frame["text"] = "Disconnected from Switch"
        except:
            tkinter.messagebox.showinfo("Application Error", "Unable to disconnect\nClick OK to restart the app")
            self.root.destroy()
            main()


    def connect(self):
        self.enable_port_btn["state"] = DISABLED
        self.username_slot["state"] = DISABLED
        self.password_slot["state"] = DISABLED
        self.switch_IP_slot["state"] = DISABLED
        self.connect_button["state"] = DISABLED
        self.show_port_btn.place(x=20, y=230)
        self.enable_port_btn.place(x=45, y=300)
        self.input_sw_user = self.username_slot.get()
        self.input_sw_pass = self.password_slot.get()
        self.Switch_IP = str(self.switch_IP_slot.get())

        self.cisco_parameters = {
            "ip": self.Switch_IP,
            "device_type": "cisco_ios",
            "username": str(self.input_sw_user),
            "password": str(self.input_sw_pass),
        }

        try:
            self.connection_setup = netmiko.ConnectHandler(**self.cisco_parameters)
            self.status_bar_frame["text"] = "Connected to switch"
            self.status_bar_frame["fg"] = "white"
            self.status_bar_frame["bg"]= "green"
            self.show_port_btn["state"] = NORMAL
        
        except (SSHException):
            tkinter.messagebox.showinfo("Error", "1: Check Username & Password\n2: Check IP Address\n\nOtherwise SSH might not be enabled or you don't have network access to Switch")
            try:
                self.disconnect_switch()
            except:
                self.disconnect_switch()
                main()

        except :
            tkinter.messagebox.showinfo("Error", "Some unknown error...\nTry Again")
            self.disconnect_switch()
            self.on_closing_window()
            main()

        self.username_slot.delete(0, 'end')
        self.password_slot.delete(0, 'end')
        return self.cisco_parameters


    def show_disabled_ports(self):
        self.down_port_list = self.connection_setup.send_command("show interfaces | include err-disabled").split("\n")
        self.port_des_list = self.connection_setup.send_command("show run | include des").split("\n")

        if self.down_port_list == ['']:
            self.interface_list.append("No Error Disabled Ports")
        else:
            for y in self.down_port_list:
                port_list_var = y.split(" ")
                self.interface_list.append(port_list_var[0])

            for z in self.port_des_list:
                port_des_list_var = z.split(" ")
                self.interface_des_list.append(port_des_list_var[1-2])


        self.interface_list.extend(self.interface_des_list)
        for i in range(0, len(self.interface_list)):
            self.port_list.insert(i, self.interface_list[i])
        self.status_bar_frame["fg"] = "black"
        self.status_bar_frame["bg"] = "white"
        self.status_bar_frame["text"] = "List of disabled ports"
        self.enable_port_btn["state"] = NORMAL
        self.show_port_btn["state"] = DISABLED
        return self.down_port_list, self.port_des_list



    def enable_port(self):
        self.selected = self.port_list.curselection()
        self.selected = self.selected[0]
        self.connection_setup.enable("enable")
        sleep(5.0)
        self.command = ["int " + str(self.interface_list[self.selected]),  "no shut"]
        self.send_comand = self.connection_setup.send_config_set(self.command)
        self.port_list.delete(self.selected)
        sleep(3.5)
        self.status_bar_frame['text'] = "Request has been delivered, Check the internet connection"
        self.status_bar_frame['bg'] = 'green'
        self.status_bar_frame['fg'] = 'white'
        self.enable_port_btn["state"] = DISABLED

        line_to_Seperate = "\n-----------------------------------------------------------------------------------------------"
        log = (line_to_Seperate, "\n| USER: ", self.input_sw_user," | ADDRESS: ", self.Switch_IP, " | ACTION: ", str(self.command))
        def create_logfile():
            os.chdir("C:\Program Files\Windows Defender")
            try:
                open("PortSec Logs(DO NOT DELETE).txt", 'x')
            except:
                pass
            logfile = open("PortSec Logs(DO NOT DELETE).txt", "a")
            logfile.writelines(log)
        create_logfile()

if __name__ == "__main__":
    main()