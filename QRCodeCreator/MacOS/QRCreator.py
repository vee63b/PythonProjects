import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk, ImageDraw, ImageOps

def generate_qr_code(qr_type):
    round_corners = round_var.get()
    add_frame = frame_var.get()

    if qr_type == "URL":
        url = url_entry.get()
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

    elif qr_type == "Contact Card":
        # Gather contact information
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        mobile_phone = mobile_phone_entry.get()
        business_phone = business_phone_entry.get()
        personal_email = personal_email_entry.get()
        business_email = business_email_entry.get()
        address = address_entry.get()
        
        # Construct vCard information string
        vcard_info = f"BEGIN:VCARD\nVERSION:3.0\nN:{last_name};{first_name}\nTEL;TYPE=CELL:{mobile_phone}\nTEL;TYPE=WORK:{business_phone}\nEMAIL;TYPE=HOME:{personal_email}\nEMAIL;TYPE=WORK:{business_email}\nADR:{address}\nEND:VCARD"

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(vcard_info)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

    elif qr_type == "WiFi":
        ssid = ssid_entry.get()
        password = password_entry.get()
        security_type = security_combobox.get()
        wifi_config = f"WIFI:S:{ssid};T:{security_type};P:{password};;"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(wifi_config)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

    elif qr_type == "Social Media QR":
        # Construct social media information string
        # Assuming round and frame options are not applicable for Social Media QR
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(social_media_info)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

    if round_corners:
        # Convert the image to RGBA mode
        img = img.convert("RGBA")

        # Create a mask for the round shape
        mask = Image.new("L", (img.size[0], img.size[1]), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

        # Apply the mask to the image
        img = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
        rounded_img = Image.new("RGBA", img.size)
        rounded_img.paste(img, (0, 0), mask)
        img = rounded_img

    if add_frame:
        # Add frame around the QR code
        img = add_frame_around_qr(img)

    img.save("qr_code.png")
    status_label.config(text=f"{qr_type} QR code generated successfully!")
    preview_qr_code("qr_code.png")

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
        frame_toggle.grid(row=2, column=0, padx=2, pady=5)
        generate_url_button.grid(row=3, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=4, columnspan=2, padx=5, pady=5)
    elif qr_type == "Contact Card":
        # Show Contact Card fields
        first_name_label.grid(row=1, column=0, padx=5, pady=5)
        first_name_entry.grid(row=1, column=1, padx=5, pady=5)
        last_name_label.grid(row=2, column=0, padx=5, pady=5)
        last_name_entry.grid(row=2, column=1, padx=5, pady=5)
        mobile_phone_label.grid(row=3, column=0, padx=5, pady=5)
        mobile_phone_entry.grid(row=3, column=1, padx=5, pady=5)
        business_phone_label.grid(row=4, column=0, padx=5, pady=5)
        business_phone_entry.grid(row=4, column=1, padx=5, pady=5)
        personal_email_label.grid(row=5, column=0, padx=5, pady=5)
        personal_email_entry.grid(row=5, column=1, padx=5, pady=5)
        business_email_label.grid(row=6, column=0, padx=5, pady=5)
        business_email_entry.grid(row=6, column=1, padx=5, pady=5)
        address_label.grid(row=7, column=0, padx=5, pady=5)
        address_entry.grid(row=7, column=1, padx=5, pady=5)
        frame_toggle.grid(row=8, column=0, padx=2, pady=5)
        generate_contact_button.grid(row=9, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=10, columnspan=2, padx=5, pady=5)
    elif qr_type == "WiFi":
        # Show WiFi fields
        ssid_label.grid(row=1, column=0, padx=5, pady=5)
        ssid_entry.grid(row=1, column=1, padx=5, pady=5)
        password_label.grid(row=2, column=0, padx=5, pady=5)
        password_entry.grid(row=2, column=1, padx=5, pady=5)
        security_label.grid(row=3, column=0, padx=5, pady=5)
        security_combobox.grid(row=3, column=1, padx=10, pady=5)
        frame_toggle.grid(row=4, column=0, padx=2, pady=5)
        generate_wifi_button.grid(row=5, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=6, columnspan=2, padx=5, pady=5)
    elif qr_type == "Social Media QR":
        # Show Social Media QR fields
        facebook_label.grid(row=1, column=0, padx=5, pady=5)
        facebook_entry.grid(row=1, column=1, padx=5, pady=5)
        instagram_label.grid(row=2, column=0, padx=5, pady=5)
        instagram_entry.grid(row=2, column=1, padx=5, pady=5)
        tiktok_label.grid(row=3, column=0, padx=5, pady=5)
        tiktok_entry.grid(row=3, column=1, padx=5, pady=5)
        snapchat_label.grid(row=4, column=0, padx=5, pady=5)
        snapchat_entry.grid(row=4, column=1, padx=5, pady=5)
        twitter_label.grid(row=5, column=0, padx=5, pady=5)
        twitter_entry.grid(row=5, column=1, padx=5, pady=5)
        whatsapp_label.grid(row=6, column=0, padx=5, pady=5)
        whatsapp_entry.grid(row=6, column=1, padx=5, pady=5)
        threads_label.grid(row=7, column=0, padx=5, pady=5)
        threads_entry.grid(row=7, column=1, padx=5, pady=5)
        frame_toggle.grid(row=8, column=0, padx=2, pady=5)
        generate_social_media_button.grid(row=9, columnspan=2, padx=5, pady=5)
        cancel_button.grid(row=10, columnspan=2, padx=5, pady=5)

def hide_all_fields():
    for widget in input_frame.winfo_children():
        widget.grid_forget()

def reset_app():
    root.destroy()
    main()

def reset_dropdowns():
    qr_type.set(qr_type["values"][0])

def add_frame_around_qr(img):
    # Add frame around the QR code
    draw = ImageDraw.Draw(img)
    width, height = img.size
    border_width = 10
    draw.rectangle([border_width, border_width, width - border_width, height - border_width], outline="black", width=3)
    return img

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
    qr_type = ttk.Combobox(input_frame, values=["Contact Card", "Social Media QR", "URL", "WiFi"])
    qr_type.grid(row=0, column=1, padx=5, pady=5)
    qr_type.bind("<<ComboboxSelected>>", lambda event: show_fields(qr_type.get()))

    # URL fields
    global url_label, url_entry, generate_url_button
    url_label = ttk.Label(input_frame, text="URL:")
    url_entry = ttk.Entry(input_frame, width=50)
    generate_url_button = ttk.Button(input_frame, text="Generate URL QR Code", command=lambda: generate_qr_code("URL"))

    # Contact Card fields
    global first_name_label, first_name_entry, last_name_label, last_name_entry, mobile_phone_label, mobile_phone_entry
    global business_phone_label, business_phone_entry, personal_email_label, personal_email_entry, business_email_label, business_email_entry
    global address_label, address_entry, generate_contact_button
    first_name_label = ttk.Label(input_frame, text="First Name:")
    first_name_entry = ttk.Entry(input_frame, width=50)
    last_name_label = ttk.Label(input_frame, text="Last Name:")
    last_name_entry = ttk.Entry(input_frame, width=50)
    mobile_phone_label = ttk.Label(input_frame, text="Mobile Phone:")
    mobile_phone_entry = ttk.Entry(input_frame, width=50)
    business_phone_label = ttk.Label(input_frame, text="Business Phone:")
    business_phone_entry = ttk.Entry(input_frame, width=50)
    personal_email_label = ttk.Label(input_frame, text="Personal Email:")
    personal_email_entry = ttk.Entry(input_frame, width=50)
    business_email_label = ttk.Label(input_frame, text="Business Email:")
    business_email_entry = ttk.Entry(input_frame, width=50)
    address_label = ttk.Label(input_frame, text="Address:")
    address_entry = ttk.Entry(input_frame, width=50)
    generate_contact_button = ttk.Button(input_frame, text="Generate Contact Card QR Code", command=lambda: generate_qr_code("Contact Card"))

    # WiFi fields
    global ssid_label, ssid_entry, password_label, password_entry, security_label, security_combobox, generate_wifi_button
    ssid_label = ttk.Label(input_frame, text="SSID:")
    ssid_entry = ttk.Entry(input_frame, width=50)
    password_label = ttk.Label(input_frame, text="Password:")
    password_entry = ttk.Entry(input_frame, show="*")
    security_label = ttk.Label(input_frame, text="Security Type:")
    security_combobox = ttk.Combobox(input_frame, values=["WEP", "WPA", "WPA2"])
    generate_wifi_button = ttk.Button(input_frame, text="Generate WiFi QR Code", command=lambda: generate_qr_code("WiFi"))

    # Social Media QR fields
    global facebook_label, facebook_entry, instagram_label, instagram_entry, tiktok_label, tiktok_entry
    global snapchat_label, snapchat_entry, twitter_label, twitter_entry, whatsapp_label, whatsapp_entry, threads_label, threads_entry
    global generate_social_media_button
    facebook_label = ttk.Label(input_frame, text="Facebook:")
    facebook_entry = ttk.Entry(input_frame, width=50)
    instagram_label = ttk.Label(input_frame, text="Instagram:")
    instagram_entry = ttk.Entry(input_frame, width=50)
    tiktok_label = ttk.Label(input_frame, text="TikTok:")
    tiktok_entry = ttk.Entry(input_frame, width=50)
    snapchat_label = ttk.Label(input_frame, text="Snapchat:")
    snapchat_entry = ttk.Entry(input_frame, width=50)
    twitter_label = ttk.Label(input_frame, text="Twitter:")
    twitter_entry = ttk.Entry(input_frame, width=50)
    whatsapp_label = ttk.Label(input_frame, text="WhatsApp:")
    whatsapp_entry = ttk.Entry(input_frame, width=50)
    threads_label = ttk.Label(input_frame, text="Threads:")
    threads_entry = ttk.Entry(input_frame, width=50)
    generate_social_media_button = ttk.Button(input_frame, text="Generate Social Media QR Code", command=lambda: generate_qr_code("Social Media QR"))

    # Cancel button
    global cancel_button
    cancel_button = ttk.Button(input_frame, text="Cancel", command=reset_app)

    # Status label
    global status_label
    status_label = ttk.Label(root, text="")
    status_label.pack(padx=10, pady=5)

    # Round toggle
    global round_var, round_toggle
    round_var = tk.BooleanVar()
    round_toggle = ttk.Checkbutton(input_frame, text="Round", variable=round_var)

    # Frame toggle
    global frame_var, frame_toggle
    frame_var = tk.BooleanVar()
    frame_toggle = ttk.Checkbutton(input_frame, text="Frame", variable=frame_var)

    root.mainloop()

if __name__ == "__main__":
    main()
