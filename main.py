import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import re
import smtplib
from email.message import EmailMessage
import os

con = mysql.connector.connect(host="localhost",
                            user="root",
                            passwd="abc123",
                            database="project")

cur = con.cursor(buffered=True)

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Login")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("400x400")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "PageOne":
            self.geometry("444x795")
            self.title("Registration")
            self.frames["PageOne"].clear_all()
        elif page_name == "PageTwo":
            self.geometry("700x700")
            self.title("Home")
        elif page_name == "StartPage":
            self.geometry("400x400")
            self.title("Login")
            self.frames["StartPage"].clear_all()
        frame.tkraise()

    def pass_on_text(self, data):
        self.frames["PageTwo"].get_text(data)

    

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        a = tk.Label(self, text="")
        a.grid(row=0)

        self.usr = tk.Label(self, text="Username:", width=12)
        self.usr.grid(row=1, column=1, pady=10)

        self.usr_in = tk.Entry(self, width=23)
        self.usr_in.grid(row=1, column=2, pady=10)

        self.psw = tk.Label(self, text="Password:", width=12)
        self.psw.grid(row=2, column=1)

        self.psw_in = tk.Entry(self, width=23, show="●")
        self.psw_in.grid(row=2, column=2, pady=10)

        val = tk.Label(self,text='')
        val.grid(row=3, column=2, columnspan=3)
            
        sub = tk.Button(self, text="Login", width=12, command=lambda: login())
        sub.grid(row=4, column=2, padx=20, columnspan=3, pady=10)

        crt = tk.Button(self, text="Create New Account", command=lambda: controller.show_frame("PageOne"))
        crt.grid(row=5, column=2, padx=20, columnspan=3)

        def send_text(data):
            controller.pass_on_text(data)
            
        def login():
            u = self.usr_in.get()
            pw = self.psw_in.get()
            a = (u,)
            if u=='' or pw=='':
                val.configure(text="All fields are required.")
            else:
                val.configure(text="")
                query = """select password from users where user = %s"""
                cur.execute(query, a)
                pas = cur.fetchone()
                if pas:                
                    p = pas[0]
                    if p == pw:
                        query = """select fname from user_details where user = %s"""
                        cur.execute(query, a)
                        a = cur.fetchone()
                        send_text([u, a[0]])
                        
                        controller.show_frame("PageTwo")
                    else:
                        messagebox.showerror("Error","Wrong password.")
                else:
                    messagebox.showerror("User not found.","Please check your username or create new account.")

    def clear_all(self):
        self.usr_in.delete(0,'end')
        self.psw_in.delete(0,'end')
    


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        user_details = tk.LabelFrame(self, text="User Details")
        user_details.pack(fill="both")

        self.usrnm = tk.Label(user_details, text="Username:", anchor='e')
        self.usrnm.grid(row=2, column=1, pady=10)

        def username_val(char):
            return char.isalnum() or char == "_"

        validate_user = user_details.register(username_val)

        self.usrnm_in = tk.Entry(user_details, width=23, validate="key", validatecommand=(validate_user, '%S'))
        self.usrnm_in.grid(row=2, column=2, pady=10, columnspan=2)
        
        self.fname = tk.Label(user_details, text="First Name:", anchor='e')
        self.fname.grid(row=3, column=1, pady=10)

        def only_alpha(char):
            return char.isalpha()

        validation = user_details.register(only_alpha)

        self.fname_in = tk.Entry(user_details, width=23, validate="key", validatecommand=(validation, '%S'))
        self.fname_in.grid(row=3, column=2, pady=10, columnspan=2)

        self.lname = tk.Label(user_details, text="Last Name:", anchor='e')
        self.lname.grid(row=4, column=1, pady=10)

        self.lname_in = tk.Entry(user_details, width=23, validate="key", validatecommand=(validation, '%S'))
        self.lname_in.grid(row=4, column=2, pady=10, columnspan=2)

        self.gender = tk.Label(user_details, text="Gender:", anchor='e')
        self.gender.grid(row=5, column=1, pady=10)

        self.gen = tk.StringVar()

        self.male = tk.Radiobutton(user_details, text="Male", value='Male', var=self.gen)
        self.male.grid(row=5, column=2, pady=10, padx=0)

        self.female = tk.Radiobutton(user_details, text="Female", value='Female', var=self.gen)
        self.female.grid(row=5, column=3, pady=10)

        self.gen.set("Male")
        
        self.pswd = tk.Label(user_details, text="Password:", anchor='e')
        self.pswd.grid(row=6, column=1)

        self.pswd_in = tk.Entry(user_details, width=23, show="●")
        self.pswd_in.grid(row=6, column=2, pady=10, columnspan=2)

        self.con_pswd = tk.Label(user_details, text="Confirm password:", anchor='e')
        self.con_pswd.grid(row=7, column=1)

        self.con_pswd_in = tk.Entry(user_details, width=23, show="●")
        self.con_pswd_in.grid(row=7, column=2, pady=10, columnspan=2)

        self.email = tk.Label(user_details, text='Email:', anchor='e')
        self.email.grid(row=8, column=1, pady=10)
            
        self.email_in = tk.Entry(user_details, width=23)
        self.email_in.grid(row=8, column=2, pady=10, columnspan=2)

        self.ph = tk.Label(user_details, text="Phone: ", anchor='e')
        self.ph.grid(row=9, column=1, pady=10)

        phonere = re.compile(r'^[0-9]{1,10}$')

        def is_phone(data):
            return phonere.match(data) != None
                
        validate_phone = user_details.register(is_phone)


        self.ph_in = tk.Entry(user_details, width=23, validate="key", validatecommand=(validate_phone, '%P'))
        self.ph_in.grid(row=9, column=2, pady=10, columnspan=2)

        bsn = tk.LabelFrame(self, text="Business Details")
        bsn.pack(fill="both",padx=4)

        self.business = tk.Label(bsn, text='Business Name:', anchor='e')
        self.business.grid(row=1, column=1, pady=10)

        self.business_in = tk.Entry(bsn, width=23)
        self.business_in.grid(row=1, column=2, pady=10)

        self.address = tk.Label(bsn, text='Business Address:', anchor="n")
        self.address.grid(row=2, column=1, pady=10)

        self.address_in = tk.Text(bsn, width=20, height=5)
        self.address_in.grid(row=2, column=2, pady=10)

        state = tk.Label(bsn, text="State:", width=20)
        state.grid(row=3, column=1, pady=10)

        def location(char):
            return char.isalpha() or char == " "

        validation_loc = bsn.register(location)
        
        self.state_in = tk.Entry(bsn, width=23, validate="key", validatecommand=(validation_loc, '%S'))
        self.state_in.grid(row=3, column=2, padx=20)

        city = tk.Label(bsn, text="City:")
        city.grid(row=4, column=1, pady=10)
        
        self.city_in = tk.Entry(bsn, width=23, validate="key", validatecommand=(validation_loc, '%S'))
        self.city_in.grid(row=4, column=2, pady=10)

        
        self.bph = tk.Label(bsn, text="Business Phone: ", anchor='e')
        self.bph.grid(row=5, column=1, pady=10)

        self.bph_in = tk.Entry(bsn, width=23, validate="key", validatecommand=(validate_phone, '%P'))
        self.bph_in.grid(row=5, column=2, pady=10)

        self.reg = tk.Button(self, text="Register", width=12, command=lambda: register())
        self.reg.pack()
        
        self.back = tk.Button(self, text="Back to Login", command=lambda: controller.show_frame("StartPage"))
        self.back.pack()

        def register():
            user = self.usrnm_in.get()
            f = self.fname_in.get()
            l = self.lname_in.get()
            pwd = self.pswd_in.get()
            con_pwd = self.con_pswd_in.get()
            eml = self.email_in.get()
            gn = self.gen.get()
            print(gn)
            phn = self.ph_in.get()
            bs = self.business_in.get()
            ad = self.address_in.get('1.0','end')
            st = self.state_in.get()
            ct = self.city_in.get()
            bphn = self.bph_in.get()
            u = (user, pwd)
            u_details = (user, f, l, eml, gn, phn, bs)

            if user and f and l and pwd and con_pwd and eml and gn and phn and bs and ad and st and ct and bphn:
                q = """select * from users where user = %s"""
                uname = (user, )
                cur.execute(q, uname)
                if cur.rowcount > 0:
                    messagebox.showerror("Error", "Username already exists. Please enter a different username.")
                else:
                    if pwd == con_pwd:
                        path = "./address/" + user + ".txt"
                        try:
                            q = """insert into users (user, password) values(%s,%s)"""
                            cur.execute(q, u)
                            q1 = """insert into user_details (user, fname, lname, email, gender, phone, business) values(%s,%s,%s,%s,%s,%s,%s)"""
                            cur.execute(q1, u_details)
                            business = (bs, user, path, ct, st, bphn)
                            q2 = """insert into businesses (name, user, address, city, state, phone) values(%s,%s,%s,%s,%s,%s)"""
                            cur.execute(q2, business)
                            f = open(path, 'w')
                            f.write(ad)
                            # q3 = "create table " + user + " (id int auto_increment primary key, fname varchar(20), lname varchar(20), email varchar(30),phone varchar(20), address varchar(70), state varchar(25), city varchar(20))"
                            # cur.execute(q3)
                            con.commit()
                            messagebox.showinfo("Registration Successful","Your account has been created.")
                            controller.show_frame("StartPage")
                        except mysql.connector.Error as error:
                            if os.path.isfile(path):
                                os.remove(path)
                            print(error)
                    else:
                        messagebox.showerror("Error", "Passwords do not match.")
                                            
            else:
                messagebox.showerror("Error", "Please enter all fields")

    def clear_all(self):
        self.usrnm_in.delete(0,'end')
        self.fname_in.delete(0,'end')
        self.fname_in.delete(0,'end')
        self.lname_in.delete(0,'end')
        self.pswd_in.delete(0,'end')
        self.con_pswd_in.delete(0,'end')
        self.email_in.delete(0,'end')
        self.gen.set("male")
        self.ph_in.delete(0,'end')
        self.business_in.delete(0,'end')
        self.address_in.delete(1.0,'end')
        self.state_in.delete(0,'end')
        self.city_in.delete(0,'end')
        self.bph_in.delete(0,'end')
        

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        self.user = ''
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.label = tk.Label(self, text= "", font=controller.title_font)
        self.label.pack()
        
        self.business_details = tk.LabelFrame(self, text="Business Details")
        self.business_details.pack(fill="both")
        
        self.add = tk.Label(self.business_details, text="Address:")
        self.add.grid(row=1, column=0, sticky='nw', padx='10', pady='5')
        
        self.user_add = tk.Label(self.business_details, text="", justify='left')
        self.user_add.grid(row=1, column=1, sticky='w')

        self.ph = tk.Label(self.business_details, text="Phone:")
        self.ph.grid(row=2, column=0, sticky='nw', padx='10', pady='5')

        self.user_ph = tk.Label(self.business_details, text="", justify='left')
        self.user_ph.grid(row=2, column=1, sticky='w')

        self.user_details = tk.LabelFrame(self, text="User Details")
        self.user_details.pack(fill="both")

        self.name = tk.Label(self.user_details, text="Name:")
        self.name.grid(row=1, column=0,sticky='nw', padx='10', pady='5')

        self.user_name = tk.Label(self.user_details, text="", justify='left')
        self.user_name.grid(row=1, column=1,sticky='w')

        self.email = tk.Label(self.user_details, text="Email:")
        self.email.grid(row=2, column=0,sticky='nw', padx='10', pady='5')

        self.user_email = tk.Label(self.user_details, text="", justify='left')
        self.user_email.grid(row=2, column=1,sticky='w')

        self.gender = tk.Label(self.user_details, text="Gender:")
        self.gender.grid(row=3, column=0,sticky='nw', padx='10', pady='5')

        self.user_gender = tk.Label(self.user_details, text="", justify='left')
        self.user_gender.grid(row=3, column=1,sticky='w')

        self.phone = tk.Label(self.user_details, text="Phone:", justify='left')
        self.phone.grid(row=4, column=0, sticky='nw', padx='10', pady='5')

        self.user_phone = tk.Label(self.user_details, text="")
        self.user_phone.grid(row=4, column=1,sticky='w')

        self.customers = tk.LabelFrame(self, text="Customers")
        self.customers.pack(fill="both")

        self.add = tk.Button(self.customers, text="Add", width=12, command=lambda: self.create_customer())
        self.add.grid(row=1, column=0, sticky='nw', padx='10', pady='5')

        self.show_cust = tk.Button(self.customers, text="View", width=12, command=lambda: self.search_customers())
        self.show_cust.grid(row=1, column=1, sticky='nw', padx='10', pady='5')

        self.logout = tk.Button(self, text="Logout", command=lambda: controller.show_frame("StartPage"))
        self.logout.pack()

    def search_customers(self):
        search_cust = tk.Toplevel(self)
        search_cust.geometry('800x700')
        search_cust.title('Search Customers')

        search = tk.LabelFrame(search_cust, text="Search Customers")
        search.pack(fill="both")

        search_label = tk.Label(search, text="Search:")
        search_label.grid(row=0, column=0, padx='5', pady='5')

        search_in = tk.Entry(search)
        search_in.grid(row=0, column=1, padx='5', pady='5')

        search_parameters = ['ID', 'First Name', 'Last Name', 'Email', 'Phone', 'City', 'State']
        
        search_by = ttk.Combobox(search, text="Search by...", values=search_parameters)
        search_by.grid(row=0, column=2, padx='5', pady='5')
        search_by.set('ID')

        search_button = tk.Button(search, text="Search Customers", command=lambda: view_all("search"))
        search_button.grid(row=0, column=3, padx='5', pady='5')

        all_button = tk.Button(search, text="View All Customers", command=lambda: view_all("all"))
        all_button.grid(row=0, column=4, padx='5', pady='5')

        results = tk.LabelFrame(search_cust, text="Results")
        results.pack(fill="both")

        def view_all(op):

            for child in results.winfo_children():
                child.destroy()

            s = op
            id_label = tk.Label(results, text="ID", justify='right')
            id_label.grid(row=0, column=0, padx='5', pady='5', sticky='w')
            n_label = tk.Label(results, text="Name")
            n_label.grid(row=0, column=1, padx='5', pady='5')

            l = tk.Label(results, text="")
            l.grid(row=1, column=1, columnspan=3)
            
            data = (self.user, )
            if op == "all":
                query = "select id, fname, lname from customers where user = %s"
            elif op == "search":
                para = search_by.get()
                searchbox = search_in.get()
                data = (self.user, "%" + searchbox + "%")
                if para == 'ID':
                    query = "select id, fname, lname from customers where user = %s and id = %s"
                    data = (self.user, searchbox)
                elif para == 'First Name':
                    query = "select id, fname, lname from customers where user = %s and fname like %s"
                elif para == 'Last Name':
                    query = "select id, fname, lname from customers where user = %s and lname like %s"
                elif para == 'Email':
                    query = "select id, fname, lname from customers where user = %s and email = %s"
                    data = (self.user, searchbox)
                elif para == 'Phone':
                    query = "select id, fname, lname from customers where user = %s and phone = %s"
                    data = (self.user, searchbox)
                elif para == 'City':
                    query = "select id, fname, lname from customers where user = %s and city like %s"
                elif para == 'State':
                    query = "select id, fname, lname from customers where user = %s and state like %s"
            else:
                return
                
            cur.execute(query, data)
            r = cur.fetchall()
            res_length = len(r)
            if res_length == 0:
                l = tk.Label(results, text="No results found...")
                l.grid(row=1, column=1, columnspan=3)
            arr = []
            for i in range(res_length):
                for j in range(0,2):
                    name = r[i][1] + " " + r[i][2]
                    a = [r[i][0], name]
                    r_label = tk.Label(results, text=a[j])
                    r_label.grid(row=i+1,column=j, padx='7', pady='7', sticky='w')
                    if j == 1:
                        d = (self.user, a[0])
                        arr.append(d)
                        
                        def view_details(d):

                            some_d = d
                            
                            query = "select * from customers where user = %s and id = %s"
                            cur.execute(query, d)
                            c_details = cur.fetchone()
                            view = tk.Toplevel(search_cust)
                            view.geometry('400x500')
                            view.title('Customer Details')

                            info = tk.Label(view, text= "Customer Details", font=self.controller.title_font)
                            info.pack()

                            info_frame = tk.LabelFrame(view)
                            info_frame.pack(fill='both')

                            cid = tk.Label(info_frame, text="ID:")
                            cid.grid(row=0,column=0, padx='7', pady='7', sticky='w')
                            cust_cid = tk.Label(info_frame, text=c_details[0],justify='left')
                            cust_cid.grid(row=0,column=1, sticky='w', columnspan=2)
                            
                            name = tk.Label(info_frame, text="Name:")
                            name.grid(row=1,column=0, padx='7', pady='7', sticky='w')
                            cust_name = tk.Label(info_frame, text=c_details[1] + " " + c_details[2],justify='left')
                            cust_name.grid(row=1,column=1, sticky='w', columnspan=2)

                            email = tk.Label(info_frame, text="Email:")
                            email.grid(row=2,column=0, padx='7', pady='7', sticky='w')
                            cust_email = tk.Label(info_frame, text=c_details[3],justify='left')
                            cust_email.grid(row=2,column=1, sticky='w')

                            def compose_email():
                                to_email = tk.Toplevel(view)
                                to_email.geometry("400x400")
                                to_email.title("Email Login")
                                

                                a = tk.Label(to_email, text="Login to your email")
                                a.grid(row=0, column=1)
                                
                                email_id = tk.Label(to_email, text="Email:",justify='left')
                                email_id.grid(row=1, column=0, pady=10, sticky='w')

                                email_id_in = tk.Entry(to_email, width=27,justify='left')
                                email_id_in.grid(row=1, column=1, pady=10, sticky='w')
                                email_id_in.insert(0, self.user_email["text"])
                                email_id_in.config(state='readonly')

                                psword = tk.Label(to_email, text="Password:",justify='left')
                                psword.grid(row=2, column=0, sticky='w')

                                psword_in = tk.Entry(to_email, width=27, show="●",justify='left')
                                psword_in.grid(row=2, column=1, pady=10, sticky='w')

                                val = tk.Label(to_email,text='')
                                val.grid(row=3, column=1, columnspan=3)

                                def compose():
                                    s=smtplib.SMTP("smtp.gmail.com",587)
                                    s.starttls()
                                    if psword_in == "":
                                        val.config(text="Enter password.")
                                    else:
                                        try:
                                            s.login(email_id_in.get(),psword_in.get())
                                        except Exception as e:
                                            val.config(text="Wrong Password.")
                                            print(e)

                                        a.grid_remove()
                                        email_id.grid_remove()
                                        email_id_in.grid_remove()
                                        psword.grid_remove()
                                        psword_in.grid_remove()
                                        val.grid_remove()
                                        sub.grid_remove()
                                        
                                        to_email.geometry("715x500")
                                        to_email.title("Compose Email")

                                        from_label = tk.Label(to_email, text="From:",justify='left')
                                        from_label.grid(row=0, column=0, pady=5, sticky='w')

                                        from_id = tk.Entry(to_email, width=50, justify='left')
                                        from_id.grid(row=0, column=1, pady=5, sticky='w')
                                        from_id.insert(0, email_id_in.get())
                                        from_id.config(state='readonly')

                                        to_label = tk.Label(to_email, text="To:",justify='left')
                                        to_label.grid(row=1, column=0, pady=5, sticky='w')

                                        to_id = tk.Entry(to_email, width=50, justify='left')
                                        to_id.grid(row=1, column=1, pady=5, sticky='w')
                                        to_id.insert(0, cust_email['text'])

                                        subject = tk.Label(to_email, text="Subject:",justify='left')
                                        subject.grid(row=2, column=0, pady=5, sticky='w')

                                        subject_in = tk.Entry(to_email, width=50,justify='left')
                                        subject_in.grid(row=2, column=1, pady=5, sticky='w')

                                        mail = tk.Text(to_email, width=70, height= 12)
                                        mail.grid(row=3, column=0, columnspan=2, sticky='w')

                                        def send_it():
                                            msg=EmailMessage()
                                            msg['Subject'] = subject_in.get()
                                            msg['from'] = email_id_in.get()
                                            msg['to'] = to_id.get()
                                            msg.set_content(mail.get('1.0','end'))
                                            s.send_message(msg)
                                            messagebox.showinfo("Sent","Message sent successfully.")
                                            to_email.destroy()

                                        send_mail = tk.Button(to_email, text="Send", command=lambda: send_it(),justify='left',width=20)
                                        send_mail.grid(row=4, column=0, pady=5, sticky='w')

                                        cancel = tk.Button(to_email, text="Cancel", command=lambda: to_email.destroy(),justify='left',width=20)
                                        cancel.grid(row=4, column=1, pady=5, sticky='w')
                                    
                                    
                                sub = tk.Button(to_email, text="Login", width=12, command=lambda: compose())
                                sub.grid(row=4, column=1, pady=10)

                                to_email.mainloop()
                                

                            send_email = tk.Button(info_frame, text="Send Email", command=lambda:compose_email())
                            send_email.grid(row=2,column=2, sticky='w', padx="20")

                            phone = tk.Label(info_frame, text="Phone:")
                            phone.grid(row=3,column=0, padx='7', pady='7', sticky='w')
                            cust_phone = tk.Label(info_frame, text=c_details[4],justify='left')
                            cust_phone.grid(row=3,column=1, sticky='w', columnspan=2)
                            
                            f = open(c_details[5],'r')
                            address = f.read()
                            f.close()
                            add = tk.Label(info_frame, text="Address:")
                            add.grid(row=4,column=0, padx='7', pady='7', sticky='nw')
                            cust_add = tk.Label(info_frame, text=address + c_details[7] + ",\n" + c_details[6], justify='left')
                            cust_add.grid(row=4,column=1, sticky='w', columnspan=2)

                            update_button = tk.Button(view, text="Update", width=60, command=lambda: update_cust())
                            update_button.pack(padx=10)


                            def update_cust():
                                a = [cust_cid["text"], cust_name["text"], cust_email["text"], cust_phone["text"], cust_add["text"]]
                                cust_name.grid_remove()
                                cust_email.grid_remove()
                                cust_phone.grid_remove()
                                cust_add.grid_remove()
                                
                                cust_name_edit = tk.Entry(info_frame, width=20)
                                cust_name_edit.grid(row=1,column=1, sticky='w')
                                cust_name_edit.insert(0,a[1])

                                cust_email_edit = tk.Entry(info_frame, width=20)
                                cust_email_edit.grid(row=2,column=1, sticky='w')
                                cust_email_edit.insert(0,a[2])
                                
                                cust_phone_edit = tk.Entry(info_frame, width=20)
                                cust_phone_edit.grid(row=3,column=1, sticky='w')
                                cust_phone_edit.insert(0,a[3])

                                cust_add_edit = tk.Text(info_frame, width=20, height=5)
                                cust_add_edit.grid(row=4,column=1, sticky='w')
                                cust_add_edit.insert(1.0,a[4])

                                update_button.pack_forget()
                                delete_button.pack_forget()
                                    
                                def save_changes():
                                    message = messagebox.askquestion('Update customer','Do you want to save the changes?', icon='warning')
                                    if message == 'yes':
                                        try:
                                            ch_n = cust_name_edit.get()
                                            f_l_name = ch_n.split()
                                            ch_e = cust_email_edit.get()
                                            ch_ph = cust_phone_edit.get()
                                            ch_ad = cust_add_edit.get('1.0', 'end')
                                            if ch_ad != a[4]:
                                                lines = ch_ad.splitlines()
                                                ch_st = lines.pop()
                                                ch_ct = lines.pop()
                                                ct_len = len(ch_ct)
                                                ch_ct = ch_ct[:ct_len - 1]
                                                ch_ad = lines[0] + "\n"
                                                lines.pop(0)
                                                for i in lines:
                                                    ch_ad += i + "\n"
                                                    
                                                if ch_ph == a[3]:
                                                    del_ch_path = "./customers/" + self.user + "/" + a[3] + ".txt"
                                                    f = open(del_ch_path,'w')
                                                    f.write(ch_ad)
                                                    f.close()
                                                    ch_values = (f_l_name[0], f_l_name[1], ch_e, ch_st, ch_ct, ch_ph, a[0])
                                                    up_query = "update customers set fname = %s, lname = %s, email = %s, state = %s, city = %s, phone = %s where id = %s"
                                                    cur.execute(up_query,  ch_values)
                                                    con.commit()
                                                    messagebox.showinfo('Update','The customer data has been updated.')
                                                    view.destroy()
                                                    view_details(some_d)

                                                else:
                                                    del_ch_path = "./customers/" + self.user + "/" + a[3] + ".txt"
                                                    if os.path.isfile(del_ch_path):
                                                        os.remove(del_ch_path)
                                                    del_ch_path = "./customers/" + self.user + "/" + ch_ph + ".txt"
                                                    f = open(del_ch_path,'w')
                                                    f.write(ch_ad)
                                                    f.close()
                                                    ch_values = (f_l_name[0], f_l_name[1], ch_e, ch_st, ch_ct, del_ch_path, ch_ph, a[0])
                                                    up_query = "update customers set fname = %s, lname = %s, email = %s, state = %s, city = %s, address = %s, phone = %s where id = %s"
                                                    cur.execute(up_query,  ch_values)
                                                    con.commit()
                                                    messagebox.showinfo('Update','The customer data has been updated.')
                                                    view.destroy()
                                                    view_details(some_d)
                                            else:
                                                if ch_ph == a[3]:
                                                    ch_values = (f_l_name[0], f_l_name[1], ch_e, a[0])
                                                    up_query = "update customers set fname = %s, lname = %s, email = %s where id = %s"
                                                    cur.execute(up_query,  ch_values)
                                                    con.commit()
                                                else:
                                                    new_path = "./customers/" + self.user + "/" + ch_ph + ".txt"
                                                    os.rename(r"./customers/" + self.user + "/" + a[3] + ".txt",r"./customers/" + self.user + "/" + ch_ph + ".txt")
                                                    ch_values = (f_l_name[0], f_l_name[1], ch_e, new_path, ch_ph, a[0])
                                                    up_query = "update customers set fname = %s, lname = %s, email = %s, address = %s, phone = %s, where id = %s"
                                                    cur.execute(up_query,  ch_values)
                                                    con.commit()

                                                messagebox.showinfo('Update','The customer data has been updated.')
                                                view.destroy()
                                                view_details(some_d)
                                                    

                                        except mysql.connector.Error as error:
                                            print(error)
                                    else:
                                        pass
                                    
                                set_button = tk.Button(view, text="Save Changes", width=60, command=lambda: save_changes())
                                set_button.pack(padx=10)

                            def delete_cust():
                                message = messagebox.askquestion('Delete customer','Are you sure you want to delete this customer?', icon='warning')
                                if message == 'yes':
                                    try:
                                        del_path= "./customers/" + self.user + "/" + cust_phone["text"] + ".txt"
                                        cust = (cust_cid["text"], )
                                        view.destroy()
                                        if os.path.isfile(del_path):
                                            os.remove(del_path)
                                        del_query = 'delete from customers where id = %s'
                                        cur.execute(del_query, cust)
                                        con.commit()
                                        messagebox.showinfo('Deleted','The customer has been deleted.')
                                        view_all(s)
                                        
                                    except mysql.connector.Error as error:
                                        print(error)
                                else:
                                    pass
                                                  
                            delete_button = tk.Button(view, text="Delete", width=60, command=lambda: delete_cust())
                            delete_button.pack(padx=10) 
                            view.mainloop()
                            
                        viewbutton = tk.Button(results, text="View",command=lambda i=i: view_details(arr[i]), width=30)    
                        viewbutton.grid(row=i+1, column=j+1, padx='7', pady='7', sticky='w')

                           

        id_label = tk.Label(results, text="ID")
        id_label.grid(row=0, column=0, padx='5', pady='5')
        n_label = tk.Label(results, text="Name", justify='left')
        n_label.grid(row=0, column=1, padx='5', pady='5', sticky='w')

    def create_customer(self):
        add_cust = tk.Toplevel(self)
        add_cust.geometry('450x500')

        add_cust.title("Add Customer")
        
        fname = tk.Label(add_cust, text="First Name:", justify='right')
        fname.grid(row=1, column=0, padx=8, pady=10, sticky='w')

        def only_alpha(char):
            return char.isalpha()

        validation = add_cust.register(only_alpha)

        fname_in = tk.Entry(add_cust, width=23, validate="key", validatecommand=(validation, '%S'))
        fname_in.grid(row=1, column=1, pady=10, columnspan=2)

        lname = tk.Label(add_cust, text="Last Name:", justify='right')
        lname.grid(row=2, column=0, padx=8, pady=10, sticky='w')

        lname_in = tk.Entry(add_cust, width=23, validate="key", validatecommand=(validation, '%S'))
        lname_in.grid(row=2, column=1, pady=10, columnspan=2)

        email = tk.Label(add_cust, text='Email:', justify='right')
        email.grid(row=3, column=0, padx=8, pady=10, sticky='w')

        email_in = tk.Entry(add_cust, width=23)
        email_in.grid(row=3, column=1, pady=10, columnspan=2)

        phone = tk.Label(add_cust, text='Phone:', justify='right')
        phone.grid(row=4, column=0, padx=8, pady=10, sticky='w')

        phonere = re.compile(r'^[0-9]{1,10}$')

        def is_phone(data):
            return phonere.match(data) != None
                
        validate_phone = add_cust.register(is_phone)

        phone_in = tk.Entry(add_cust, width=23, validate="key", validatecommand=(validate_phone, '%P'))
        phone_in.grid(row=4, column=1, pady=10, columnspan=2)

        address = tk.Label(add_cust, text='Address:', anchor="n", justify='right')
        address.grid(row=5, column=0, padx=8, pady=10, sticky='w')
        
        address_in = tk.Text(add_cust, width=19, height=5)
        address_in.grid(row=5, column=1, pady=10, padx=7, columnspan=2)

        state = tk.Label(add_cust, text="State:", justify='right')
        state.grid(row=6, column=0, padx=8, pady=10, sticky='w')

        def location(char):
            return char.isalpha() or char == " "

        validation_loc = add_cust.register(location)
        
        state_in = tk.Entry(add_cust, width=23, validate="key", validatecommand=(validation_loc, '%S'))
        state_in.grid(row=6, column=1, pady=10, columnspan=2)

        city = tk.Label(add_cust, text="City:", justify='right')
        city.grid(row=7, column=0, padx=8, pady=10, sticky='w')
        
        city_in = tk.Entry(add_cust, width=23, validate="key", validatecommand=(validation_loc, '%S'))
        city_in.grid(row=7, column=1, pady=10, columnspan=2)

        req = tk.Label(add_cust,text="")
        req.grid(row=8, column=1)

        def customer():
            if fname_in and lname_in and email_in and phone_in and address_in and state_in and city_in:
                req.config(text="")
                fn = fname_in.get()
                ln = lname_in.get()
                em = email_in.get()
                ph = phone_in.get()
                ad = address_in.get('1.0','end')
                st = state_in.get()
                ct = city_in.get()
                path = "./customers/" + self.user
                if not os.path.isdir(path):
                     os.mkdir(path)
                path2= path + "/" + ph + ".txt"
                f = open(path2,'w')
                f.write(ad)
                f.close()
                details = (fn, ln, em, ph, path2, st, ct, self.user)
                try:
                    cur.execute("insert into customers (fname, lname, email, phone, address, state, city, user) values(%s,%s,%s,%s,%s,%s,%s,%s)", details)
                    con.commit()
                except mysql.connector.Error as error:
                    if os.path.isfile(path2):
                        os.remove(path2)
                    print(error)
                messagebox.showinfo("Created","Customer added successfully.")
                add_cust.destroy()

            else:
                req.config(text="All fields are required.")

        create = tk.Button(add_cust, text="Create", width=12, command=lambda: customer())
        create.grid(row=8, column=1, sticky='nw', padx='10', pady='10')

        cancel = tk.Button(add_cust, text="Cancel", width=12, command=lambda: add_cust.destroy())
        cancel.grid(row=8, column=2, sticky='nw', padx='10', pady='10')
        
        add_cust.mainloop()     
        
        
    def get_text(self, data):
        self.user = data[0]
        cur.execute('select name, city, state, phone, address from businesses where user = %s', (self.user,))
        bname = cur.fetchone()
        self.label.config(text=bname[0])
        f = open(bname[4],'r')
        a = f.readlines()
        add = ""
        for i in a:
            add += i
        add = add + bname[1] + ",\n" + bname[2]
        f.close()
        self.user_add.config(text=add)
        self.user_ph.config(text=bname[3])
        cur.execute('select fname, lname, email, gender, phone from user_details where user = %s', (self.user,))
        uname = cur.fetchone()
        name = uname[0] + " " + uname[1]
        self.user_name.config(text=name)
        self.user_email.config(text=uname[2])
        self.user_gender.config(text=uname[3])
        self.user_phone.config(text=uname[4])
        
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
