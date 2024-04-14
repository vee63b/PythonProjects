import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr_code(qr_type):
    if qr_type == "URL":
        url = url_entry.get()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("url_qr_code.png")
        status_label.config(text="URL QR code generated successfully!")
        preview_qr_code("url_qr_code.png")
    elif qr_type == "Download Link":
        download_link = download_link_entry.get()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(download_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("download_qr_code.png")
        status_label.config(text="Download QR code generated successfully!")
        preview_qr_code("download_qr_code.png")
    elif qr_type == "Contact Card":
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        contact_info = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(contact_info)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("contact_card_qr_code.png")
        status_label.config(text="Contact card QR code generated successfully!")
        preview_qr_code("contact_card_qr_code.png")
    elif qr_type == "WiFi":
        ssid = ssid_entry.get()
        password = password_entry.get()
        security_type = security_combobox.get()
        wifi_config = f"WIFI:S:{ssid};T:{security_type};P:{password};;"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(wifi_config)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("wifi_qr_code.png")
        status_label.config(text="WiFi QR code generated successfully!")
        preview_qr_code("wifi_qr_code.png")

def preview_qr_code(image_path):
    preview_window = tk.Toplevel(root)
    preview_window.title("QR Code Preview")

    img = Image.open(image_path)
    img.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    qr_label = tk.Label(preview_window, image=img_tk)
    qr_label.image = img_tk
    qr_label.pack(padx=10, pady=10)

    save_button = ttk.Button(preview_window, text="Save QR Code", command=lambda: save_qr_code(image_path))
    save_button.pack(side="left", padx=5, pady=5)

    cancel_button = ttk.Button(preview_window, text="Cancel", command=preview_window.destroy)
    cancel_button.pack(side="right", padx=5, pady=5)

def save_qr_code(image_path):
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if save_path:
        img = Image.open(image_path)
        img.save(save_path)
        status_label.config(text=f"QR code saved to: {save_path}")

def show_fields(qr_type):
    hide_all_fields()
    if qr_type == "URL":
        url_label.grid(row=1, column=0, padx=5, pady=5)
        url_entry.grid(row=1, column=1, padx=5, pady=5)
        generate_url_button.grid(row=2, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=3, columnspan=2, padx=5, pady=5)
    elif qr_type == "Download Link":
        download_link_label.grid(row=1, column=0, padx=5, pady=5)
        download_link_entry.grid(row=1, column=1, padx=5, pady=5)
        generate_download_button.grid(row=2, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=3, columnspan=2, padx=5, pady=5)
    elif qr_type == "Contact Card":
        name_label.grid(row=1, column=0, padx=5, pady=5)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        phone_label.grid(row=2, column=0, padx=5, pady=5)
        phone_entry.grid(row=2, column=1, padx=5, pady=5)
        email_label.grid(row=3, column=0, padx=5, pady=5)
        email_entry.grid(row=3, column=1, padx=5, pady=5)
        generate_contact_button.grid(row=4, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=5, columnspan=2, padx=5, pady=5)
    elif qr_type == "WiFi":
        ssid_label.grid(row=1, column=0, padx=5, pady=5)
        ssid_entry.grid(row=1, column=1, padx=5, pady=5)
        password_label.grid(row=2, column=0, padx=5, pady=5)
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        security_label.grid(row=3, column=0, padx=5, pady=5)
        security_combobox.grid(row=3, column=1, padx=5, pady=5)
        generate_wifi_button.grid(row=4, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=5, columnspan=2, padx=5, pady=5)

def hide_all_fields():
    for widget in input_frame.winfo_children():
        widget.grid_forget()

def reset_app():
    root.destroy()
    main()

def reset_dropdowns():
    qr_type.set(qr_type["values"][0])

def main():
    global root
    root = tk.Tk()
    root.title("QR Code Generator")

    # Create input frame
    global input_frame
    input_frame = ttk.Frame(root)
    input_frame.pack(padx=10, pady=10)

    # QR code type selection
    ttk.Label(input_frame, text="QR Code Type:").grid(row=0, column=0, padx=5, pady=5)
    global qr_type
    qr_type = ttk.Combobox(input_frame, values=["URL", "Download Link", "Contact Card", "WiFi"])
    qr_type.grid(row=0, column=1, padx=5, pady=5)
    qr_type.bind("<<ComboboxSelected>>", lambda event: show_fields(qr_type.get()))

    # URL fields
    global url_label, url_entry, generate_url_button
    url_label = ttk.Label(input_frame, text="URL:")
    url_entry = ttk.Entry(input_frame, width=50)
    generate_url_button = ttk.Button(input_frame, text="Generate URL QR Code", command=lambda: generate_qr_code("URL"))

    # Download link fields
    global download_link_label, download_link_entry, generate_download_button
    download_link_label = ttk.Label(input_frame, text="Download Link:")
    download_link_entry = ttk.Entry(input_frame, width=50)
    generate_download_button = ttk.Button(input_frame, text="Generate Download QR Code", command=lambda: generate_qr_code("Download Link"))

    # Contact card fields
    global name_label, name_entry, phone_label, phone_entry, email_label, email_entry, generate_contact_button
    name_label = ttk.Label(input_frame, text="Name:")
    name_entry = ttk.Entry(input_frame, width=50)
    phone_label = ttk.Label(input_frame, text="Phone:")
    phone_entry = ttk.Entry(input_frame, width=50)
    email_label = ttk.Label(input_frame, text="Email:")
    email_entry = ttk.Entry(input_frame, width=50)
    generate_contact_button = ttk.Button(input_frame, text="Generate Contact Card QR Code", command=lambda: generate_qr_code("Contact Card"))

    # WiFi fields
    global ssid_label, ssid_entry, password_label, password_entry, security_label, security_combobox, generate_wifi_button
    ssid_label = ttk.Label(input_frame, text="SSID:")
    ssid_entry = ttk.Entry(input_frame, width=50)
    password_label = ttk.Label(input_frame, text="Password:")
    password_entry = ttk.Entry(input_frame, show="*")  # Password entry with hidden characters
    security_label = ttk.Label(input_frame, text="Security Type:")
    security_combobox = ttk.Combobox(input_frame, values=["WEP", "WPA", "WPA2"])
    generate_wifi_button = ttk.Button(input_frame, text="Generate WiFi QR Code", command=lambda: generate_qr_code("WiFi"))

    # Cancel button
    global cancel_button
    cancel_button = ttk.Button(input_frame, text="Cancel", command=reset_app)

    # Status label
    global status_label
    status_label = ttk.Label(root, text="")
    status_label.pack(padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
