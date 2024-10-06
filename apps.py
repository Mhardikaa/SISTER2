import tkinter as tk
from tkinter import messagebox
import threading
import time

# Fungsi untuk animasi pengiriman pesan Request-Response
def request_response(sender, receiver, log):
    # Menampilkan pesan bahwa pengirim mengirim pesan ke penerima
    log.insert(tk.END, f"{sender} mengirim pesan ke {receiver}...\n")
    root.update()  # Memperbarui tampilan GUI
    time.sleep(1)  # Menunggu selama 1 detik
    
    # Menampilkan pesan bahwa penerima menerima pesan dari pengirim
    log.insert(tk.END, f"{receiver} menerima pesan dari {sender}.\n")
    root.update()  # Memperbarui tampilan GUI
    time.sleep(1)  # Menunggu selama 1 detik
    
    # Menampilkan pesan bahwa penerima mengirim respons ke pengirim
    log.insert(tk.END, f"{receiver} mengirim respons ke {sender}...\n")
    root.update()  # Memperbarui tampilan GUI
    time.sleep(1)  # Menunggu selama 1 detik
    
    # Menampilkan pesan bahwa pengirim menerima respons dari penerima
    log.insert(tk.END, f"{sender} menerima respons dari {receiver}.\n")
    root.update()  # Memperbarui tampilan GUI
    time.sleep(1)  # Menunggu selama 1 detik
    
    # Menampilkan pesan bahwa komunikasi selesai
    log.insert(tk.END, "Komunikasi selesai.\n\n")

# Fungsi untuk memulai simulasi Request-Response
def start_request_response():
    sender = entry_sender.get()  # Mengambil nama pengirim dari input
    receiver = entry_receiver.get()  # Mengambil nama penerima dari input
    
    # Memeriksa apakah input tidak kosong
    if not sender or not receiver:
        messagebox.showwarning("Input Error", "Nama pengirim dan penerima tidak boleh kosong!")
        return  # Menghentikan eksekusi fungsi jika ada kesalahan
    
    log_request.delete(1.0, tk.END)  # Bersihkan log
    # Memulai thread baru untuk menjalankan fungsi request_response
    threading.Thread(target=request_response, args=(sender, receiver, log_request)).start()

# Fungsi untuk animasi Publish-Subscribe
def publish_message(publisher, message, log):
    # Menampilkan pesan bahwa publisher mempublikasikan pesan
    log.insert(tk.END, f"{publisher} mempublikasikan pesan: '{message}'...\n")
    root.update()  # Memperbarui tampilan GUI
    time.sleep(1)  # Menunggu selama 1 detik
    
    # Mengirim pesan ke semua subscriber
    for subscriber in subscribers:
        log.insert(tk.END, f"{subscriber} menerima pesan: '{message}'.\n")
        root.update()  # Memperbarui tampilan GUI
        time.sleep(1)  # Menunggu selama 1 detik
    
    log.insert(tk.END, "Pesan diterima oleh semua subscriber.\n\n")

# Fungsi untuk memulai simulasi Publish-Subscribe
def start_publish_subscribe():
    publisher = entry_publisher.get()  # Mengambil nama publisher dari input
    message = entry_message.get()  # Mengambil pesan dari input
    
    # Memeriksa apakah input tidak kosong
    if not publisher or not message:
        messagebox.showwarning("Input Error", "Publisher dan pesan tidak boleh kosong!")
        return  # Menghentikan eksekusi fungsi jika ada kesalahan
    
    # Memeriksa apakah ada subscriber
    if len(subscribers) == 0:
        messagebox.showwarning("Subscriber Error", "Harus ada setidaknya satu subscriber.")
        return  # Menghentikan eksekusi fungsi jika tidak ada subscriber
    
    log_publish.delete(1.0, tk.END)  # Bersihkan log
    # Memulai thread baru untuk menjalankan fungsi publish_message
    threading.Thread(target=publish_message, args=(publisher, message, log_publish)).start()

# Fungsi untuk menambahkan subscriber
def add_subscriber():
    subscriber = entry_subscriber.get()  # Mengambil nama subscriber dari input
    # Memeriksa apakah subscriber tidak kosong dan belum ditambahkan
    if subscriber and subscriber not in subscribers:
        subscribers.append(subscriber)  # Menambahkan subscriber ke daftar
        listbox_subscribers.insert(tk.END, subscriber)  # Menampilkan subscriber di listbox
        entry_subscriber.delete(0, tk.END)  # Mengosongkan input subscriber
    else:
        messagebox.showwarning("Input Error", "Subscriber tidak boleh kosong atau sudah ditambahkan.")

# Fungsi untuk menghapus subscriber yang dipilih
def remove_subscriber():
    selected_subscriber = listbox_subscribers.curselection()  # Mendapatkan subscriber yang dipilih
    if selected_subscriber:
        subscriber = listbox_subscribers.get(selected_subscriber)  # Mengambil nama subscriber yang dipilih
        subscribers.remove(subscriber)  # Menghapus subscriber dari daftar
        listbox_subscribers.delete(selected_subscriber)  # Menghapus dari listbox
    else:
        messagebox.showwarning("Selection Error", "Pilih subscriber yang akan dihapus.")

# Fungsi untuk mengganti tampilan sesuai model komunikasi yang dipilih
def switch_model(selection):
    if selection == "Request-Response":
        frame_request_response.tkraise()  # Tampilkan frame Request-Response
    else:
        frame_publish_subscribe.tkraise()  # Tampilkan frame Publish-Subscribe

# Setup GUI Tkinter
root = tk.Tk()  # Membuat instance Tkinter
root.title("Simulasi Model Komunikasi")  # Menetapkan judul aplikasi

# Variabel untuk menyimpan subscriber
subscribers = []

# Dropdown untuk memilih model komunikasi
selected_model = tk.StringVar()
selected_model.set("Request-Response")  # Set default model

# Dropdown menu untuk memilih model
dropdown = tk.OptionMenu(root, selected_model, "Request-Response", "Publish-Subscribe", command=switch_model)
dropdown.grid(row=0, column=0, padx=10, pady=10)  # Menempatkan dropdown di grid

# Frame untuk Request-Response
frame_request_response = tk.Frame(root, padx=10, pady=10)
frame_request_response.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Label dan input untuk pengirim dan penerima
tk.Label(frame_request_response, text="Request-Response").grid(row=0, column=0, columnspan=2)
tk.Label(frame_request_response, text="Nama Pengirim:").grid(row=1, column=0, sticky="e")
entry_sender = tk.Entry(frame_request_response)
entry_sender.grid(row=1, column=1)

tk.Label(frame_request_response, text="Nama Penerima:").grid(row=2, column=0, sticky="e")
entry_receiver = tk.Entry(frame_request_response)
entry_receiver.grid(row=2, column=1)

# Tombol untuk memulai simulasi Request-Response
tk.Button(frame_request_response, text="Mulai Simulasi", command=start_request_response).grid(row=3, column=0, columnspan=2)

# Text area untuk log Request-Response
log_request = tk.Text(frame_request_response, width=40, height=10)
log_request.grid(row=4, column=0, columnspan=2)

# Frame untuk Publish-Subscribe
frame_publish_subscribe = tk.Frame(root, padx=10, pady=10)
frame_publish_subscribe.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Label dan input untuk publisher dan pesan
tk.Label(frame_publish_subscribe, text="Publish-Subscribe").grid(row=0, column=0, columnspan=2)
tk.Label(frame_publish_subscribe, text="Publisher:").grid(row=1, column=0, sticky="e")
entry_publisher = tk.Entry(frame_publish_subscribe)
entry_publisher.grid(row=1, column=1)

tk.Label(frame_publish_subscribe, text="Pesan:").grid(row=2, column=0, sticky="e")
entry_message = tk.Entry(frame_publish_subscribe)
entry_message.grid(row=2, column=1)

# Tombol untuk mempublikasikan pesan
tk.Button(frame_publish_subscribe, text="Publikasikan Pesan", command=start_publish_subscribe).grid(row=3, column=0, columnspan=2)

# Text area untuk log Publish-Subscribe
log_publish = tk.Text(frame_publish_subscribe, width=40, height=10)
log_publish.grid(row=4, column=0, columnspan=2)

# Frame untuk mengelola subscriber
frame_subscriber = tk.Frame(frame_publish_subscribe, padx=10, pady=10)
frame_subscriber.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

tk.Label(frame_subscriber, text="Subscribers").grid(row=0, column=0, columnspan=2)

# Input untuk menambahkan subscriber
entry_subscriber = tk.Entry(frame_subscriber)
entry_subscriber.grid(row=1, column=0, columnspan=2)

# Tombol untuk menambah dan menghapus subscriber
tk.Button(frame_subscriber, text="Tambah Subscriber", command=add_subscriber).grid(row=2, column=0, columnspan=2)
tk.Button(frame_subscriber, text="Hapus Subscriber", command=remove_subscriber).grid(row=3, column=0, columnspan=2)

# Listbox untuk menampilkan daftar subscriber
listbox_subscribers = tk.Listbox(frame_subscriber, height=6)
listbox_subscribers.grid(row=4, column=0, columnspan=2)

# Atur frame request-response sebagai frame yang pertama kali muncul
frame_request_response.tkraise()

# Memulai loop utama Tkinter
root.mainloop()
