
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


# ===================== DATA MODEL =====================

class Resident:
    def __init__(self, name, student_id, contact):
        self.name = name
        self.student_id = student_id
        self.contact = contact

    def __str__(self):
        return f"{self.name} ({self.student_id}) - {self.contact}"


class Node:
    def __init__(self, resident):
        self.resident = resident
        self.next = None

    def to_list(self):
        result = []
        cur = self.head
        while cur:
            result.append(cur.resident)
            cur = cur.next
        return result

# Node for Singly Linked-List
class Node:
    def __init__(self, resident):
        self.resident = resident
        self.next = None

# Singly Linked List for current residents
class ResidentLinkedList:
    def __init__(self):
        self.head = None
#adding residents
    def add_resident(self, resident):
        new_node = Node(resident)
        new_node.next = self.head
        self.head = new_node
#removing residents
    def remove_resident(self, student_id):
        current = self.head
        previous = None

           while current:
            if current.resident.student_id == student_id:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return current.resident
            previous = current
            current = current.next
        return None

    def display_residents(self):
        current = self.head
        if not current:
            print("No residents in hostel.")
            return
        while current:
            print(current.resident)
            current = current.next

class WaitingQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, resident):
        self.queue.append(resident)

    def dequeue(self):
        return self.queue.pop(0) if self.queue else None

    def to_list(self):
        return list(self.queue)


class HostelManager:
    def __init__(self, capacity):
        self.capacity = capacity
        self.current_count = 0
        self.residents = ResidentLinkedList()
        self.waiting = WaitingQueue()

    def check_in(self, resident):
        if self.current_count < self.capacity:
            self.residents.add_resident(resident)
            self.current_count += 1
            return "checked_in"
        else:
            self.waiting.enqueue(resident)
            return "queued"

    def check_out(self, student_id):
        removed = self.residents.remove_resident(student_id)
        if not removed:
            return ("not_found", None)

        self.current_count -= 1
        moved_in = None

        if self.waiting.to_list():
            moved_in = self.waiting.dequeue()
            self.residents.add_resident(moved_in)
            self.current_count += 1

        return ("checked_out", moved_in)

# -------- Queue --------
class Queue:
    def _init_(self):
        self.front = None
        self.rear = None

    def enqueue(self, resident):
        node = Node(resident)
        if not self.rear:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node

    def dequeue(self):
        if not self.front:
            return None
        temp = self.front
        self.front = self.front.next
        if not self.front:
            self.rear = None
        return temp.resident

    def search(self, student_id):
        current = self.front
        while current:
            if current.resident.student_id == student_id:
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.front
        while current:
            result.append(str(current.resident))
            current = current.next
        return result

    def search_with_position(self, student_id):
        current = self.front
        position = 1
        while current:
            if current.resident.student_id == student_id:
                return current.resident, position
            current = current.next
            position += 1
        return None, -1

# ===================== MAIN APP =====================
class HostelApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hostel Check-in & Check-out Management System")

        self.state("zoomed")          # ✅ OPTION 2: MAXIMIZED WINDOW
        self.resizable(True, True)    # allow resizing


        self.manager = HostelManager(capacity=3)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (WelcomePage, MainMenuPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(WelcomePage)

    def show_frame(self, page):
        self.frames[page].tkraise()


# ===================== PAGE 1 : WELCOME =====================
class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # ===== AUTO-RESIZE BACKGROUND IMAGE =====
        w = controller.winfo_screenwidth()
        h = controller.winfo_screenheight()

        img = Image.open("images/dsa_image.png")
        img = img.resize((w, h))
        self.bg_image = ImageTk.PhotoImage(img)

        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        tk.Label(
            self,
            text="HOSTEL MANAGEMENT ONLINE SYSTEM (HOMS)",
            font=("Arial", 20, "bold"),
            bg="white"
        ).place(relx=0.5, y=80, anchor="center")

        ttk.Button(
            self,
            text="Proceed to Hostel Management",
            width=30,
            command=lambda: controller.show_frame(MainMenuPage)
        ).place(relx=0.5, y=260, anchor="center")


# ===================== PAGE 2 : MAIN MENU =====================

class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(
            self,
            text="Hostel Check-In & Check-Out Management",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        form = ttk.LabelFrame(self, text="Resident Details")
        form.pack(padx=20, pady=10, fill="x")

        self.name = tk.StringVar()
        self.sid = tk.StringVar()
        self.contact = tk.StringVar()

        ttk.Label(form, text="Name").grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(form, textvariable=self.name).grid(row=0, column=1)

        ttk.Label(form, text="Student ID").grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(form, textvariable=self.sid).grid(row=1, column=1)

        ttk.Label(form, text="Contact").grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(form, textvariable=self.contact).grid(row=2, column=1)

        ttk.Button(form, text="Check In", command=self.check_in).grid(row=0, column=3, padx=20)
        ttk.Button(form, text="Check Out", command=self.check_out).grid(row=1, column=3)

        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.resident_list = tk.Listbox(list_frame, width=45)
        self.resident_list.pack(side="left", padx=10)

        self.waiting_list = tk.Listbox(list_frame, width=45)
        self.waiting_list.pack(side="right", padx=10)

        ttk.Button(
            self,
            text="Back to Welcome Page",
            command=lambda: controller.show_frame(WelcomePage)
        ).pack(pady=10)

        self.controller = controller
        self.refresh()

    def refresh(self):
        self.resident_list.delete(0, tk.END)
        for r in self.controller.manager.residents.to_list():
            self.resident_list.insert(tk.END, str(r))

        self.waiting_list.delete(0, tk.END)
        for r in self.controller.manager.waiting.to_list():
            self.waiting_list.insert(tk.END, str(r))

    def check_in(self):
        if not self.name.get() or not self.sid.get() or not self.contact.get():
            messagebox.showwarning("Error", "All fields required")
            return

        res = Resident(self.name.get(), self.sid.get(), self.contact.get())
        result = self.controller.manager.check_in(res)

        if result == "checked_in":
            messagebox.showinfo("Success", "Resident checked in")
        else:
            messagebox.showinfo("Full", "Hostel full. Added to waiting list")

        self.refresh()

    def check_out(self):
        status, moved = self.controller.manager.check_out(self.sid.get())

        if status == "not_found":
            messagebox.showerror("Error", "Resident not found")
        else:
            msg = "Check-out successful"
            if moved:
                msg += f"\n{moved} moved in from waiting list"
            messagebox.showinfo("Done", msg)

        self.refresh()
        
   # AUTO FILL STUDENT ID WHEN CLICKED
    def select_resident(self, event):
        selected = event.widget.curselection()
        if not selected:
            return
        value = event.widget.get(selected[0])
        sid = value.split("(")[-1].replace(")", "").strip()
        self.sid.set(sid)

    def refresh(self, controller):
        self.res_list.delete(0, tk.END)
        self.wait_list.delete(0, tk.END)

        for r in controller.residents.to_list():
            self.res_list.insert(tk.END, r)

        for w in controller.waiting.to_list():
            self.wait_list.insert(tk.END, w)

    def check_in(self, controller):
        name = self.name.get()
        sid = self.sid.get()

        if not name or not sid:
            messagebox.showwarning("Input Error", "All fields required")
            return

        if controller.residents.search(sid) or controller.waiting.search(sid):
            messagebox.showerror("Duplicate", "Student already exists")
            return

        res = Resident(name, sid)

        if controller.count < controller.capacity:
            controller.residents.insert(res)
            controller.count += 1
            messagebox.showinfo("Success", "Resident checked in")
        else:
            controller.waiting.enqueue(res)
            messagebox.showinfo("Hostel Full", "Added to waiting queue")

        self.refresh(controller)

    def check_out(self, controller):
        sid = self.sid.get()
        if not sid:
            messagebox.showwarning("Error", "Select a resident first")
            return

        removed = controller.residents.delete(sid)
        if not removed:
            messagebox.showerror("Error", "Resident not found")
            return

        controller.count -= 1

        moved = controller.waiting.dequeue()
        if moved:
            controller.residents.insert(moved)
            controller.count += 1

        messagebox.showinfo("Done", "Check-out successful")
        self.sid.set("")
        self.name.set("")
        self.refresh(controller)

    def search(self, controller):
        sid = self.sid.get()

        if not sid:
            messagebox.showwarning("Input Error", "Enter Student ID")
            return

        #  Search in resident list (Linked List)
        resident = controller.residents.search(sid)
        if resident:
            messagebox.showinfo(
                "Search Result",
                f"Name: {resident.name}\n"
                f"Student ID: {resident.student_id}\n"
                f"Status: Checked-in (Resident List)"
            )
            return

        #  Search in waiting queue
        queued_resident, position = controller.waiting.search_with_position(sid)
        if queued_resident:
            messagebox.showinfo(
                "Search Result",
                f"Name: {queued_resident.name}\n"
                f"Student ID: {queued_resident.student_id}\n"
                f"Status: Waiting Queue (Position {position})"
            )
            return

        # Not found
        messagebox.showerror("Not Found", "Student not found in system")


# ===================== RUN APP =====================

if __name__ == "__main__":
    app = HostelApp()
    app.mainloop()




