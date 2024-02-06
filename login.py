from tkinter import *
from tkinter import messagebox, Checkbutton, IntVar, filedialog, RIGHT, LEFT, END
from PASSWORD import PASSWORD_ENTRY
from persiantools.jdatetime import JalaliDateTime
from datetime import datetime
import threading,time,sys,os,csv,getpass,random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from bidi.algorithm import get_display
import pyperclip


ghofl = 0
image_place = None

numberss='D:\\New folder (3)\\numbers.txt'


if numberss:
    with open(numberss, 'r', encoding='utf8') as f:
        groups = [group.strip() for group in f.readlines()]
    remaining_numbers =  len(groups)
    #update_remaining_numbers()
    

#----------------------------------------
browser_is_open=0
def open_browser():
    global browser_is_open,driver, wait,msg
    browser_is_open=1
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_argument(CHROME_PROFILE_PATH)
    # options.add_argument('--profile-directory=Profile 2')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 300)
   




def get_full_path(filename):
    try:
        if getattr(sys, 'frozen', False):
            current_directory = os.path.dirname(sys.executable)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_directory, filename)
        return file_path
    except Exception as e:
        print(f'Error getting full path: {e}')


numberss_path = get_full_path(numberss)


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content





emojis = read_file('emoji.txt')
name_of_person=None
def format_msg(msg, emojis,name_of_person=None, include_signature=True, include_gregorian=False, include_jalali=False,
        include_random_emoji=False, send_based_on_name_var=False,enable_advanced_var=False):
    msg_with_prefix=msg
    random_emoji=''
    if include_random_emoji:
        random_emoji = random.choice(emojis).strip()
        
    if enable_advanced_var and send_based_on_name_var:
        based_on_name_msg=f'سلام مخاطب {name_of_person}'


    if     enable_advanced_var and send_based_on_name_var and include_random_emoji:
        msg_with_prefix = f'{random_emoji} {based_on_name_msg} \n{msg}'
    elif enable_advanced_var and send_based_on_name_var:
        msg_with_prefix = f'{based_on_name_msg} \n{msg}'
    else:
        msg_with_prefix = f'{random_emoji} {msg}'

    if include_gregorian or include_jalali:
        if include_gregorian:
            current_date = datetime.now().strftime('%H:%M:%S---%Y-%m-%d')
            msg_with_prefix = f'\n\n\n{msg_with_prefix}⏰زمان: {current_date}\n'
        if include_jalali:
            current_date = JalaliDateTime.now().strftime('%H:%M:%S---%Y-%m-%d')
            msg_with_prefix = f'\n\n\n{msg_with_prefix}⏰زمان: {current_date}\n'
    else:
        pass
    

    if include_signature:
        # Read the signature from the signature.txt file
        signature_path = 'signature.txt'
        random_emoji = random.choice(emojis).strip()
        try:
            with open(signature_path, 'r', encoding='utf-8') as signature_file:
                signature = signature_file.read()
                msg_with_prefix += f'\n{random_emoji}\n{signature}'
        except FileNotFoundError:
            print("Signature file not found.")

    return msg_with_prefix


global activate_friendly_loop

def send():
    global msg,item,friend_numb,fmsg,activate_friendly_loop
    inp_txt_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
    input_txt_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, inp_txt_xpath)))
    print("copy msg")
    if activate_friendly_loop==0:
        pyperclip.copy(msg)
        print('msg copid')
    else:
        pyperclip.copy(fmsg)
        print(';hell ueaaa')
    input_txt_box.clear()
    input_txt_box.send_keys(Keys.CONTROL + "v")
    
    if image_place:
        time.sleep(1)
        pass
    else:
        input_txt_box.send_keys(Keys.ENTER)
        print2console(f"پیام متنی ارسال شد", lang='fa')
        if activate_friendly_loop==0:
            append_to_list(item)
        else:
            print2console("پیام متنی به دوست ارسال شد", lang='fa')
        if enable_advanced_var.get()==1:
            rnd_delay=random.randint(-5,5)
        print2console(f"وقفه به مدت {delay_value.get()+rnd_delay} ثانیه", lang='fa')
        time.sleep(delay_value+rnd_delay)


def send_image():
    global item, delay_value
    global activate_friendly_loop
    attachment_box = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@title = "Attach"]')))
    if  activate_friendly_loop==0:
        attachment_box.click()
        time.sleep(1)
        #print("injaiem")
        image_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
        #print("hala inja")
        image_box.send_keys(image_place)
        #print("youhooo")
        
        time.sleep(2)

    send_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.XPATH, '//span[@data-icon="send"]')))
    print("doghme ham payda shod")
    send_button.click()
    
    if activate_friendly_loop==0:
        append_to_list(item)
        print2console("تصویر ارسال شد", lang='fa')
    else:
        print2console("پیام به دوست ارسال شد", lang='fa')
    if enable_advanced_var.get()==1:
            rnd_delay=random.randint(-5,5)
    print2console(f"وقفه به مدت {delay_value.get()+rnd_delay} ثانیه", lang='fa')
    time.sleep(delay_value.get())
    
item=''

def get_random_friend_number():
    try:
        with open('friendly_numbers.txt', 'r', encoding='utf-8') as file:
            numbers = [line.strip() for line in file.readlines()]
            if numbers:
                return random.choice(numbers)
            else:
                return None
    except FileNotFoundError:
        print2console("شماره دوست پیدا نشد", lang='fa')
        return None


def get_random_friendly_message():
    try:
        with open('friendly_msg.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            messages = []
            current_message = None
            for line in lines:
                if line.startswith("پيام:"):
                    if current_message is not None:
                        messages.append(current_message)
                    current_message = line[6:].strip()
                elif current_message is not None:
                    print('hhhee')
                    current_message += "\n" + line.strip()
                    print('hoooo')

            if current_message is not None:
                messages.append(current_message)

            if messages:
                return random.choice(messages)
            else:
                return None
    except FileNotFoundError:
        print2console("پیام به دوست یافت نشد", lang='fa')
        return None


def extract_text_from_contact(parent_element):
    try:
        # Locate the span element within the provided parent element
        span_element = parent_element.find_element(By.XPATH, './/span[@class="enbbiyaj e1gr2w1z hp667wtd"]')

        # Extract the text content of the span element
        extracted_text = span_element.text
    except Exception as e:
        # If the specified class is not found, try extracting text directly
        extracted_text = parent_element.text

    return extracted_text

'''<div class="tvf2evcx m0h2a7mj lb5m6g5c j7l1k36l ktfrpxia nu7pwgvd p357zi0d dnb887gk gjuq5ydh i2cterl7 fhf7t426 f8m0rgwh gndfcl4n"><h2 class="q9lllk4z e1gr2w1z qfejxiq4" aria-label=""><div class="Mk0Bp _30scZ"><span dir="auto" aria-label="" class="l7jjieqr cw3vfol9 _11JPr selectable-text copyable-text" style="min-height: 0px;">Ali Amini</span></div></h2><div class="a4ywakfo qt60bha0"><span dir="auto" class="_11JPr selectable-text copyable-text"><span class="enbbiyaj e1gr2w1z hp667wtd" aria-label="">+98 937 212 9878</span></span></div></div>
<div class="tvf2evcx m0h2a7mj lb5m6g5c j7l1k36l ktfrpxia nu7pwgvd p357zi0d dnb887gk gjuq5ydh i2cterl7 fhf7t426 f8m0rgwh gndfcl4n"><h2 class="q9lllk4z e1gr2w1z qfejxiq4" aria-label=""><div class="Mk0Bp _30scZ"><span dir="auto" aria-label="" class="l7jjieqr cw3vfol9 _11JPr selectable-text copyable-text" style="min-height: 0px;">+98 993 177 9024</span></div></h2><div class="a4ywakfo qt60bha0"><span dir="auto" class="_11JPr selectable-text copyable-text"><span class="enbbiyaj e1gr2w1z hp667wtd" aria-label="">~L</span></span></div></div>
'''
def select_CHAT(index, item):
    global conditionss , name_of_person,activate_friendly_loop
    #profile_xpath='//*[@id="main"]/header/div[2]/div[1]/div'
    profile_xpath='//*[@id="main"]/header/div[1]'
    name_xpath='//*[@class="l7jjieqr cw3vfol9 _11JPr selectable-text copyable-text"]'
    #name_xpath='//*[@id="app"]/div/div[2]/div[5]/span/div/span/div/div/section/div[1]/div[2]'
    newchat_xpath = '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span'
    newchat = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, newchat_xpath)))
    newchat.click()
    #print("clicked newchat")
    search_xpath = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]'
    '''print("sleep 5 seconds")
    time.sleep(5)
    print(index)'''
    search_box = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    
    pyperclip.copy(item)
    search_box.clear()
    #print("gonna do the search")
    search_box.send_keys(Keys.CONTROL + "v")
    time.sleep(1)

    search_box.send_keys(Keys.ENTER)
    with open(numberss, "r") as input_file:
        with open("temp.txt", "w") as output_file:
            for line in input_file:
                if f'{item}' not in line.strip("\n"):
                    output_file.write(line)

    # close the input_file
    input_file.close()

    # replace file with the original name
    os.replace('temp.txt', numberss)


    try:
        # Use WebDriverWait to wait for the presence of the element
        conditionss1 = None
        #activate_friendly_loop=0
        conditionss1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "No results found for \'{item}\'")]'))
        )
        if conditionss1:
            #print("ppppp", conditionss1)
            print2console(f"شماره {item} پیدا نشد", lang='fa')
            backbtn = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/header/div/div[1]/div')))
            backbtn.click()
            conditionss = 1

    except TimeoutException:
        # Handle the case where the element is not found within the specified timeout
        conditionss = 0
        print2console(f"شماره {item} پیدا شد", lang='fa')
        append_to_list(item)
        print("hhhhh")
        update_counter_sent()
        if enable_advanced_var.get()==1:
            
            print(index)
            print(advanced_settings_entry1_value)
            print(int(index)%advanced_settings_entry1_value)
            #print2console(index % advanced_settings_entry1_value)
            if int(index) % advanced_settings_entry1_value==(index-1):
                activate_friendly_loop=1
                print2console('ارسال پیام به دوست فعال شد', lang='fa')
            else:
                activate_friendly_loop=0
                print('noooo')
        if enable_advanced_var.get()==1 and send_based_on_name_var.get()==1:
            print('sssssssssssssssiiiiiiiuuuuuuuu')
            profile = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, profile_xpath)))
            profile.click()
           
            print('SSSSSSIIIIIUUUUUUUUU')
            try:
                # Wait for the element to be present
                print('messsss')
                esm = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, name_xpath)))
                print('rrrrrrrr')
                # Extract the text from the element
                name_of_person =extract_text_from_contact(esm)
                print('bbbbbbb')
                # Extract 'L' from '~L'
                
                # Print the result
                print(name_of_person)

            except NoSuchElementException:
                name_of_person=item
                print("esm nadasht bara hamin shomare estefade mikonim")
        else:
            name_of_person=''
    update_remaining_numbers()
    time.sleep(1)



def select_CHAT_friend(friend_numb):
    global conditionss
    activate_friendly_loop=1
    newchat_xpath = '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[4]/div/span'
    newchat = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, newchat_xpath)))
    newchat.click()
    #print("clicked newchat")
    search_xpath = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]'
    
    
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    pyperclip.copy(friend_numb)
    search_box.clear()
    search_box.send_keys(Keys.CONTROL + "v")
    time.sleep(1)

    search_box.send_keys(Keys.ENTER)
    



    try:
        # Use WebDriverWait to wait for the presence of the element
        conditionss1 = None
        conditionss1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "No results found for \'{friend_numb}\'")]'))
        )
        if conditionss1:
            #print("ppppp", conditionss1)
            print2console(f"شماره {friend_numb} پیدا نشد", lang='fa')
            backbtn = wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/header/div/div[1]/div')))
            backbtn.click()
            

    except TimeoutException:
        # Handle the case where the element is not found within the specified timeout
        
        print2console(f"شماره {friend_numb} پیدا شد", lang='fa')
        #append_to_list(item)
        #print("hhhhh")
        #update_counter_sent()
        
    time.sleep(1)


#----------------------------------------------------------

def generate_user_data_dir_path(profile_number):
    username = getpass.getuser()
    
    path_template = r'user-data-dir=C:\\Users\\{}\AppData\\Local\\Google\\Chrome\\User Data\\wtsp{}'
    user_data_dir_path = path_template.format(username, profile_number)
    return user_data_dir_path
CHROME_PROFILE_PATH= r'user-data-dir=C:\\Users\\iman\AppData\\Local\\Google\\Chrome\\User Data\\wtsp'

def update_profile(*args):
    selected_profile = profile_var.get()
    global  CHROME_PROFILE_PATH
    CHROME_PROFILE_PATH = generate_user_data_dir_path(selected_profile)
    print(CHROME_PROFILE_PATH)



counter_sent=0
data_list = []

def append_to_list(number):
    global data_list
    current_time = JalaliDateTime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_list.append([number, current_time])

def save_to_csv():
    global data_list, item
    try:
        current_time = JalaliDateTime.now().strftime('%Y-%m-%d')
        csv_filename = f"{current_time}.csv"

        if getattr(sys, 'frozen', False):
            current_directory = os.path.dirname(sys.executable)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))

        csv_filepath = os.path.join(current_directory, csv_filename)

        # Create the CSV file if it doesn't exist
        if not os.path.exists(csv_filepath):
            with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Item', 'Timestamp'])

        with open(csv_filepath, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)

            # Add data to CSV file
            csv_writer.writerows(data_list)

        messagebox.showinfo("CSV Saved", f"گزارش ارسال در این آدرس ذخیره شد:\n {csv_filepath}")
        print2console(f"'گزارش ارسال در این آدرس ذخیره شد': {csv_filepath}", lang='fa')
        
        
    except Exception as e:
        messagebox.showerror("Error", f"Error saving CSV file: {e}")


def save_message_to_msg_file():
    new_message = message_entry.get("1.0", "end-1c")
    
    try:
        if getattr(sys, 'frozen', False):
            current_directory = os.path.dirname(sys.executable)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_directory, 'msg.txt')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_message)
        messagebox.showinfo("Success", "Message saved successfully!")
        message_window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Error saving message: {e}")

def open_input_window1():
    global message_window, include_text_only_var
    global  enable_advanced_var,enable_advanced_checkbox,send_based_on_name_var,send_based_on_name_checkbox,advanced_settings_entry1,advanced_settings_entry2,friendly_message_entry

    
    message_window = Toplevel(root)
    message_window.title('Edit Message')
    message_window.geometry('400x200+400+250')
    message_window.configure(bg="#37948c")
    message_window.resizable(False, False)

    if getattr(sys, 'frozen', False):
        current_directory = os.path.dirname(sys.executable)
    else:
        current_directory = os.path.dirname(os.path.abspath(__file__))
    
    file_path = os.path.join(current_directory, 'msg.txt')

    with open(file_path, 'r', encoding='utf-8') as file:
        current_message = file.read()

    global message_entry
    message_entry = Text(message_window, height=8, width=40, wrap=WORD)
    message_entry.insert("1.0", current_message)
    message_entry.pack(pady=10)

    # Checkbox to include text only
    include_text_only_var = IntVar()
    include_text_only_checkbox = Checkbutton(message_window, text='ارسال فقط متن', variable=include_text_only_var, bg='#37948c', font=('b nazanin', 12))
    include_text_only_checkbox.place(x=90,y=150)
    
    save_button = Button(message_window, text='ذخیره متن و تنطیمات', bg='#282a36', fg='white', command=save_message_and_settings)
    save_button.place(x=210,y=160)
    save_button.bind('<Enter>', onhover)
    save_button.bind('<Leave>', onleave)
    # Load the settings to set the initial state of the checkbox
    load_settings()
    init_advanced_settings_vars()


def save_message_and_settings():
    global image_place, include_text_only_var
    
    # Save the message to msg.txt
    save_message_to_msg_file()

    # delete the image place
    if include_text_only_var.get()==1:
      delete_image_path   

    # Save the settings
    save_settings(
        delay_value.get(),
        signature_var.get(),
        gregorian_var.get(),
        jalali_var.get(),
        random_emoji_var.get(),
        include_text_only_var.get(),  # Get the state of the checkbox
        number_prefix_var.get()
    )



def delete_image_path():
    global image_place
    try:
        if getattr(sys, 'frozen', False):
            current_directory = os.path.dirname(sys.executable)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_directory, 'image_place.txt')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            pass
        print2console(f"آدرس تصویر حذف شد", lang='fa')
    except Exception as e:
        messagebox.showerror("Error", f"Error saving image path: {e}")


def save_image_path():
    global image_place
    try:
        if getattr(sys, 'frozen', False):
            current_directory = os.path.dirname(sys.executable)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_directory, 'image_place.txt')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(image_place)
        print2console("تصویر انتخاب شد ", lang='fa')
        #print2console(f"{file_path}", lang='en')
    except Exception as e:
        messagebox.showerror("Error", f"Error saving image path: {e}")

def load_image_path():
    global image_place
    try:
        if getattr(sys, 'frozen', False):
            current_directory = os.path.dirname(sys.executable)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_directory, 'image_place.txt')
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                image_place = file.read()
                print2console("آدرس تصویر بارگذاری شد", lang='fa')
    except Exception as e:
        messagebox.showerror("Error", f"No Image is selected: {e}")

def select_image():
    global image_place
    load_settings()
    if include_text_only_var.get()==1:
        messagebox.showinfo("پیام متنی", f"پیام متنی ارسال میشود! لطفا در قسمت انتخاب متن تنظیمات مورد نظر را بررسی کنید ")
    else:
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        
        if file_path:
            image_place = file_path
            messagebox.showinfo("Image Selected", f"Image selected:\n{file_path}")
            save_image_path()



def write_numbers_to_file(number_prefix_var, starting_number, second_number, filename='numbers.txt'):
    end_number = starting_number + second_number
    
    try:
            
            # Get the directory of the script
            if getattr(sys, 'frozen', False):
                 current_directory= os.path.dirname(sys.executable)
            else:
                 current_directory= os.path.dirname(os.path.abspath(__file__))
            file_path= os.path.join(current_directory, filename)
                 
            load_settings()
            with open(file_path, 'a', encoding='utf-8') as file:
                for number in range(starting_number, end_number ):
                    formatted_number = number_prefix_var.get()+f'{number}\n'
                    file.write(formatted_number)
            print(f'Numbers appended to "{file_path}".')
            print2console(f'شماره‌ها اضافه شدند', lang='fa')
    except Exception as e:
            print(f'Error writing to file: {e}')

def update_remaining_numbers():
    global remaining_numbers
    with open(numberss, 'r', encoding='utf8') as f:
        groups = [group.strip() for group in f.readlines()]
    remaining_numbers = len(groups)
    remaining_label.config(text=f"شماره‌های باقی‌مانده: {remaining_numbers}")
    
def update_counter_sent():
    global counter_sent
    counter_sent=counter_sent+1
    sent_label.config(text=f"شماره‌های ارسال‌شده: {counter_sent}")
    



def resource_path(relative_path):
    try:
         base_path=sys._MEIPASS
    except Exception:
         base_path=os.path.abspath(".")
    return os.path.join(base_path,relative_path)

def read_msg():
    with open('msg.txt', 'r', encoding='utf8') as f:
        msg0 = f.read()
    return msg0
def format_friendly_messages(message):
    # Dummy function, you can replace it with the actual formatting logic
    random_emoji = random.choice(emojis).strip()
    formatted_message = f"{random_emoji}\n {message}"
    random_emoji = random.choice(emojis).strip()
    formatted_message = f" {formatted_message}\n{random_emoji}"
    return formatted_message


msg0=read_msg()
global signature_var
activate_friendly_loop=0
def send_messages_loop():
    global ghofl, remaining_numbers, conditionss, activate_friendly_loop
    while ghofl == 1 and remaining_numbers > 0:
        global  msg
        
        
        #print(msg)

        #------------------------
          
        for index, item in enumerate(groups):
            #print(index)
            load_image_path()
            if activate_friendly_loop==1 and enable_advanced_var.get()==1:
                print2console('در حال ارسال پیام به دوستان', lang='fa')
                for i in range(advanced_settings_entry2_value):
                    global  fmsg
                    friend_numb= get_random_friend_number()
                    fmsg=get_random_friendly_message()
                    fmsg=format_friendly_messages(fmsg)
                    select_CHAT_friend(friend_numb)
                    send()

                    try:
                        if image_place:
                            send_image()
                    except Exception as e:
                        print(e)
                activate_friendly_loop=0      

            #print(index)
            #print("eeeeeeeeeeeeeeeeeeeeeeee")
            try:

                conditionss = 0
                select_CHAT(index, item)
                msg = format_msg(
                    msg0,
                    emojis,
                    name_of_person,
                    include_signature=signature_var.get() == 1,
                    include_gregorian=gregorian_var.get() == 1,
                    include_jalali=jalali_var.get() == 1,
                    include_random_emoji=random_emoji_var.get() == 1,
                    send_based_on_name_var=send_based_on_name_var.get() == 1,
                    enable_advanced_var=enable_advanced_var.get() == 1
                )

                #print(conditionss)
                if conditionss == 0:
                    #print("now input box")
                    send()

                    try:
                        if image_place:
                            send_image()
                            
                    except IndexError:
                        pass
                else:
                    pass
            except Exception as e:
                print2console(e, lang='en')
                continue
        


        


        current_time = JalaliDateTime.now().strftime('%H:%M:%S---%Y-%m-%d')  # Current timestamp
        #print2console(f"{current_time}: Sending message...")
        update_remaining_numbers()
        
        time.sleep(1)


def start_sending_messages():
    global ghofl,frndly_msg
    global  enable_advanced_var,enable_advanced_checkbox,send_based_on_name_var,send_based_on_name_checkbox,advanced_settings_entry1,advanced_settings_entry2,friendly_message_entry

    ghofl = 1
    
    # Display a confirmation window
    confirmation = messagebox.askquestion("Confirmation", "آیا ارتباط با واتساپ برقرار است؟")
    
    if confirmation == 'yes':
        pass
    else:
        print2console("لطفا صبر کنید تا ارتباط برقرار شود", lang='fa')
        time.sleep(2)
        open_browser()
    
    load_settings()
    init_advanced_settings_vars()

    if enable_advanced_var.get==1:
        with open('friendly_msg.txt', 'r', encoding='utf8') as f:
            frndly_msg = f.read()
    time.sleep(5)
    
    
    messagebox.showinfo("Start Sending", "پس از تایید، ارسال پیام‌ها آغاز می‌شود")
    print2console("آغاز ارسال", lang='fa')
    threading.Thread(target=send_messages_loop).start()


def stop_sending_messages():
    global ghofl
    ghofl = 0
    messagebox.showinfo("Stop Sending", "پس از ارسال پیام فعلی، عملیات ارسال متوقف می‌شود.")
    print2console("توقف ارسال", lang='fa')




def print2console(texts, lang='en'):
    # Get the current Jalali time
    jalali_time = JalaliDateTime.now().strftime('%H:%M:%S')

    # Combine Jalali time with the input text
    

    # Configure the tag for custom font, alignment, and direction
    font = ('Times New Roman', 12) if lang == 'en' else ('b nazanin', 12)
    alignment = RIGHT if lang == 'fa' else LEFT

    console_output.config(state=NORMAL)

    # Insert the combined text with the correct font, alignment, and direction
    if lang=='en':
        console_output.insert(END, jalali_time +'---> ' , ('custom_font', 'custom_align',  'ltr'))
        console_output.insert('current', texts + '\n', ('custom_font', 'custom_align',  'ltr'))
    else:
        console_output.insert(END, texts + ' <---', ('custom_font', 'custom_align', 'rtl' ))
        console_output.insert(END,  jalali_time +' \n' , ('custom_font', 'custom_align', 'ltr' ))
 
 
    
    console_output.config(state=DISABLED)
    console_output.yview(END)
def on_btn_click():
    starting_number = int(entry_start.get())
    count = int(entry_count.get())

    write_numbers_to_file(number_prefix_var,starting_number, count)
    update_remaining_numbers() 


# Assuming you already have a function print2console similar to the previous one

def open_input_window():
    input_window = Toplevel(root)
    input_window.title('Enter Numbers')
    input_window.geometry('300x180+400+250')
    input_window.configure(bg="#37948c")
    input_window.resizable(False, False)
    
    def clear_numbers():
        # Clear the content of the numbers.txt file
        with open('numbers.txt', 'w', encoding='utf-8'):
            pass
        print2console("تمامی شماره‌ها حذف شدند", lang='fa')
        update_remaining_numbers() 

    label_start = Label(input_window, text='شماره ابتدایی (بدون پیش‌شماره)', bg='#282a36', fg='white')
    label_start.pack(pady=5)

    global entry_start
    entry_start = Entry(input_window, width=30)
    entry_start.pack(pady=5)

    label_count = Label(input_window, text='تعداد', bg='#282a36', fg='white')
    label_count.pack(pady=5)

    global entry_count
    entry_count = Entry(input_window, width=30)
    entry_count.pack(pady=5)

    submit_button = Button(input_window, text='ذخیره', bg='#282a36', fg='white', command=on_btn_click, font=('b nazanin', 10))
    submit_button.place(x=155, y=125)
    
    submit_button.bind('<Enter>', onhover)
    submit_button.bind('<Leave>', onleave)

    clear_button = Button(input_window, text='پاک کردن همه شماره‌ها', bg='#282a36', fg='white', command=clear_numbers, font=('b nazanin', 10))
    clear_button.place(x=30, y=125)
    clear_button.bind('<Enter>', onhover)
    clear_button.bind('<Leave>', onleave)

    # Add a button to view the contents of numbers.txt
    view_numbers_button = Button(input_window, text='شماره‌ها', bg='#282a36', fg='white', command=view_numbers, font=('b nazanin', 10))
    view_numbers_button.place(x=210, y=125)
    view_numbers_button.bind('<Enter>', onhover)
    view_numbers_button.bind('<Leave>', onleave)

def view_numbers():
    # Open a new window to display the contents of numbers.txt
    view_numbers_window = Toplevel(root)
    view_numbers_window.title('شماره‌ها')
    view_numbers_window.geometry('200x300+450+300')
    view_numbers_window.configure(bg="#37948c")
    view_numbers_window.resizable(False, False)

    # Create a Text widget for displaying numbers
    numbers_text = Text(view_numbers_window, wrap="word", height=16, width=25, font=('b nazanin', 12), state=DISABLED)
    numbers_text.pack()

    # Create a Scrollbar for the Text widget
    scrollbar = Scrollbar(view_numbers_window, command=numbers_text.yview)
    scrollbar.place(x=185,y=0, height=290)

    # Link the Scrollbar to the Text widget
    numbers_text.config(yscrollcommand=scrollbar.set)

    try:
        # Read the contents of numbers.txt
        with open('numbers.txt', 'r', encoding='utf-8') as numbers_file:
            numbers_content = numbers_file.read()

        # Insert the contents into the Text widget
        numbers_text.config(state=NORMAL)
        numbers_text.insert(END, numbers_content)
        numbers_text.config(state=DISABLED)
    except FileNotFoundError:
        numbers_text.config(state=NORMAL)
        numbers_text.insert(END, "شماره‌ها یافت نشدند.")
        numbers_text.config(state=DISABLED)


#----------------------------------------------------------------

root= Tk()
root.title('Login Page')
root.geometry('800x450+300+200')
root.configure(bg="#fff")
root.resizable(False,False)



number_prefix_var = StringVar(value='+98')



def signin():
    global ghofl
    username=user.get()
    password=code.get()
    with open('password.txt', 'r', encoding='utf-8') as f:
            passssword = f.readlines()
    if username=='admin' and password==PASSWORD_ENTRY:
        #print('yees')
        root.destroy()
        ghofl=1
    elif passssword[0]==PASSWORD_ENTRY:
        root.destroy()
        ghofl=1
    else:
        
        ghofl=0
    
    
        


img=PhotoImage(file=resource_path('lock.png'))
Label(root,image=img,bg='white').place(x=20,y=30)

frame=Frame(root,width=350,height=350,bg='white')
frame.place(x=430,y=50)

heading=Label(frame,text='Sign in',fg='#282a36',bg='white', font=('Microsoft Yahei UI Light',23,'bold'))
heading.place(x=90,y=0)




def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')


def onhover(event):
    event.widget['bg'] = '#3348d4'
    event.widget['fg'] = 'white'
def onhover1(event):
    event.widget['bg'] = '#8b1aab'
    event.widget['fg'] = 'white'

def onleave(event):
    event.widget['bg'] = '#282a36'
    event.widget['fg'] = 'white'

user=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
user.place(x=30,y=60)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter)
user.bind('<FocusOut>',on_leave)





Frame(frame,width=295,height=4,bg='black').place(x=25,y=80)
def on_enter(e):
    code.delete(0,'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')


code=Entry(frame,width=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light',11))
code.place(x=30,y=130)
code.insert(0,'Password')
code.bind('<FocusIn>',on_enter)
code.bind('<FocusOut>',on_leave)



Frame(frame,width=295,height=4,bg='black').place(x=25,y=150)
signin_button = Button(frame, width=39, pady=7, text='Sign in', bg='#282a36', fg='white', border=0, command=signin)
signin_button.place(x=35, y=210)

# Bind the hover and leave events to the button
signin_button.bind('<Enter>', onhover)
signin_button.bind('<Leave>', onleave)



profile_label = Label(frame, text='Choose Profile:', fg='#282a36', bg='white', font=('Microsoft Yahei UI Light', 11))
profile_label.place(x=60, y=170)

# Dropdown options for profile
profile_options = [1, 2, 3, 4]  # Add more profiles as needed
profile_var = StringVar(frame)
profile_var.set(profile_options[0])  # Default profile

profile_dropdown = OptionMenu(frame, profile_var, *profile_options)
profile_dropdown.place(x=180, y=168)
profile_dropdown.config(bg='#282a36', fg='white', font=('Microsoft Yahei UI Light', 9), border=0)
profile_dropdown['menu'].config(bg='#282a36', fg='white')

# Bind the update_profile function to the dropdown

profile_var.trace_add('write', update_profile)


#-----------------------------------------------------

root.mainloop()
if ghofl== 1:
    root= Tk()
    root.title('WhatsApp Business IYK')
    root.geometry('800x370+300+200')
    root.configure(bg="#1ddb33")

    root.resizable(False,False)
    delay_value = IntVar(value=20)
    signature_var = IntVar()
    gregorian_var = IntVar()
    jalali_var = IntVar()
    random_emoji_var = IntVar()
    number_prefix_var = StringVar()

    background_image = PhotoImage(file="background.png")

    # Create a label to display the background image
    background_label = Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)



def open_settings_window():
    global delay_value, signature_var, gregorian_var, jalali_var, random_emoji_var, number_prefix_var, signature_entry,  signature_checkbox,include_signature,include_text_only_var
    #global  enable_advanced_var,enable_advanced_checkbox,send_based_on_name_var,send_based_on_name_checkbox,advanced_settings_entry1,advanced_settings_entry2
    global  enable_advanced_var,enable_advanced_checkbox,send_based_on_name_var,send_based_on_name_checkbox,advanced_settings_entry1,advanced_settings_entry2,friendly_message_entry
    global  settings_window
    number_prefix_var = StringVar()
    random_emoji_var = IntVar()
    jalali_var = IntVar()
    gregorian_var = IntVar()
    signature_var = IntVar()
    include_text_only_var = IntVar()

    # Define IntVar for delay globally
    delay_value = IntVar()
    def enable_signature():
        include_signature = signature_var.get()
        if include_signature:
            signature_entry.config(state=NORMAL)
        else:
            signature_entry.config(state=DISABLED)

        # Save the include_signature setting
        save_settings(
        delay_value.get(),
        signature_var.get(),
        gregorian_var.get(),
        jalali_var.get(),
        random_emoji_var.get(),
        include_text_only_var.get(),  # Get the state of the checkbox
        number_prefix_var.get()
                )

    '''    
    def save_settings(delay, include_signature, include_gregorian, include_jalali, include_random_emoji, number_prefix):
        try:
            with open('settings.txt', 'w', encoding='utf-8') as settings_file:
                settings_file.write(f'delay={delay}\n')
                settings_file.write(f'include_signature={include_signature}\n')
                settings_file.write(f'include_gregorian={include_gregorian}\n')
                settings_file.write(f'include_jalali={include_jalali}\n')
                settings_file.write(f'include_random_emoji={include_random_emoji}\n')
                settings_file.write(f'number_prefix={number_prefix}\n')
            print("Settings saved.")
        except Exception as e:
            print(f'Error saving settings: {e}')
    '''
    def checkbox_command(*args):
    # Save the settings when any checkbox (except signature) is clicked
        save_settings(
        delay_value.get(),
        signature_var.get(),
        gregorian_var.get(),
        jalali_var.get(),
        random_emoji_var.get(),
        include_text_only_var.get(),  # Get the state of the checkbox
        number_prefix_var.get()
    )


    # ...

    settings_window = Toplevel(root)
    settings_window.title('تنظیمات')
    settings_window.geometry('520x260+400+250')
    settings_window.configure(bg="#37948c")
    settings_window.resizable(False, False)
    settings_window.grab_set()
    global  msg

   
    
    signature_checkbox = Checkbutton(settings_window, text='درج امضا', variable=signature_var, bg='#37948c', font=('b nazanin', 15))
    signature_checkbox.place(x=65, y=50)
    signature_checkbox.config(command=enable_signature)
    
    

    
    

    
    def save_signature():
        new_signature = signature_entry.get("1.0", "end-1c")
        with open('signature.txt', 'w', encoding='utf-8') as file:
            file.write(new_signature)
        
        # Save the include_signature setting
        save_settings(
        delay_value.get(),
        signature_var.get(),
        gregorian_var.get(),
        jalali_var.get(),
        random_emoji_var.get(),
        include_text_only_var.get(),  # Get the state of the checkbox
        number_prefix_var.get()
    )


        messagebox.showinfo("Signature Saved", f"Signature saved successfully to: signature.txt", master=settings_window)

    


    # Number delay label and entry
    delay_label = Label(settings_window, text='تاخیر:', bg='#37948c', font=('b nazanin', 15,'bold'))
    delay_label.place(x=40,y=10)

    
    delay_value.trace_add("write", checkbox_command) 
    delay_entry = Entry(settings_window, textvariable=delay_value, width=8, font=('b nazanin', 12))
    delay_entry.place(x=100,y=15)
   # delay_entry.delete(0, END)
    



    # Increase and Decrease buttons
    def increase_delay():
        current_value = delay_value.get()
        delay_value.set(current_value + 1)
        save_settings(
        delay_value.get(),
        signature_var.get(),
        gregorian_var.get(),
        jalali_var.get(),
        random_emoji_var.get(),
        include_text_only_var.get(),  # Get the state of the checkbox
        number_prefix_var.get()
    )


    def decrease_delay():
        current_value = delay_value.get()
        delay_value.set(max(0, current_value - 1))
        save_settings(
        delay_value.get(),
        signature_var.get(),
        gregorian_var.get(),
        jalali_var.get(),
        random_emoji_var.get(),
        include_text_only_var.get(),  # Get the state of the checkbox
        number_prefix_var.get()
    )


    inc_button = Button(settings_window, text='⬆', command=increase_delay,bg='#282a36',fg='white', font=('b nazanin', 7, 'bold'))
    inc_button.place(x=160,y=8)
    inc_button.bind('<Enter>', onhover)
    inc_button.bind('<Leave>', onleave)    
    dec_button = Button(settings_window, text='⬇', command=decrease_delay,bg='#282a36',fg='white', font=('b nazanin', 7,'bold'))
    dec_button.place(x=160,y=32)
    dec_button.bind('<Enter>', onhover)
    dec_button.bind('<Leave>', onleave) 
  
    

    



    signature_entry = Text(settings_window, height=6, width=40, wrap=WORD, font=('b nazanin', 12, 'bold'))
    signature_entry.place(x=10,y=85)

    # Load signature from file
    signature_filepath = 'signature.txt'
    try:
        with open(signature_filepath, 'r', encoding='utf-8') as file:
            signature_content = file.read()
            signature_entry.insert("1.0", signature_content)
    except FileNotFoundError:
        pass

    

    
    # Date format checkboxes
    
    gregorian_checkbox = Checkbutton(settings_window, text='درج تاریخ میلادی', variable=gregorian_var, bg='#37948c', font=('b nazanin', 15))
    gregorian_checkbox.place(x=360,y=20)
    gregorian_checkbox.config(command=checkbox_command)

    
    jalali_checkbox = Checkbutton(settings_window, text='درج تاریخ شمسی', variable=jalali_var, bg='#37948c', font=('b nazanin', 15))
    jalali_checkbox.place(x=360,y=55)
    jalali_checkbox.config(command=checkbox_command)

    # Random emoji checkbox
    
    random_emoji_checkbox = Checkbutton(settings_window, text='ایموجی تصادفی', variable=random_emoji_var, bg='#37948c', font=('b nazanin', 15))
    random_emoji_checkbox.place(x=360,y=90)
    random_emoji_checkbox.config(command=checkbox_command)

    # Number prefix entry
    number_prefix_label = Label(settings_window, text='پیش‌شماره', bg='#37948c', font=('b nazanin', 15))
    number_prefix_label.place(x=360,y=125)

    
    number_prefix_var = StringVar()
    number_prefix_var.trace_add("write", checkbox_command)  # Trigger the function when the variable is written
    
    number_prefix_entry = Entry(settings_window, textvariable=number_prefix_var, width=6, font=('b nazanin', 15))
    number_prefix_entry.delete(0, END)
    number_prefix_entry.insert(0, number_prefix_var.get())
    number_prefix_entry.place(x=435, y=130)
    load_settings()  
    init_advanced_settings_vars()
    # Update the content of number_prefix_entry
    

            


    save_button = Button(settings_window, text='ذخیره \n تغییرات \n امضا ',bg='#282a36',fg='white', command=save_signature, font=('b nazanin', 14,'bold'))
    save_button.place(x=254,y=85,height=160,width=70)
    save_button.bind('<Enter>', onhover)
    save_button.bind('<Leave>', onleave)    



    # Modify the button in the settings_window to open the advanced_settings_window
    advanced_settings_button = Button(settings_window, text='تنظیمات پیشرفته', bg='#282a36', fg='white', command=open_advanced_settings_window, font=('b nazanin', 14, 'bold'))
    advanced_settings_button.place(x=360, y=180)
    advanced_settings_button.bind('<Enter>', onhover)
    advanced_settings_button.bind('<Leave>', onleave)

    
    settings_window.wait_window()


include_text_only_var = IntVar()



def open_advanced_settings_window():
    global  enable_advanced_var,enable_advanced_checkbox,send_based_on_name_var,friendly_message_entry,send_based_on_name_checkbox,advanced_settings_entry1,advanced_settings_entry2

    advanced_settings_window = Toplevel(settings_window)
    advanced_settings_window.title('تنظیمات پیشرفته')
    advanced_settings_window.geometry('440x480+400+200')
    advanced_settings_window.configure(bg="#37948c")
    advanced_settings_window.resizable(False, False)


    advanced_settings_window.grab_set()
    send_based_on_name_var = IntVar()
    

    # Checkbox for enabling advanced settings
    enable_advanced_var = IntVar()
    enable_advanced_checkbox = Checkbutton(advanced_settings_window, text='فعال‌سازی ارسال پیام به دوستان', variable=enable_advanced_var, bg='#37948c', font=('b nazanin', 15))
    enable_advanced_checkbox.place(x=10, y=20)

    # Button to manage friendly numbers
    def open_friendly_numbers_window():
        friendly_numbers_window = Toplevel(advanced_settings_window)
        friendly_numbers_window.title('شماره دوستان(با پیش‌شماره)')
        friendly_numbers_window.geometry('300x300+450+250')
        friendly_numbers_window.configure(bg="#1b4d54")
        friendly_numbers_window.resizable(False, False)
        friendly_numbers_window.grab_set()
        #______________________________________________________


        # Create a Text widget for displaying numbers
        numbers_text = Text(friendly_numbers_window, wrap="word", height=16, width=25, font=('b nazanin', 12), state=NORMAL)
        numbers_text.place(x=7,y=1, height=250,width=273)

        # Create a Scrollbar for the Text widget
        scrollbar = Scrollbar(friendly_numbers_window, command=numbers_text.yview)
        scrollbar.place(x=280,y=0, height=250,width=18)

        # Link the Scrollbar to the Text widget
        numbers_text.config(yscrollcommand=scrollbar.set)

        try:
            # Read the contents of numbers.txt
            with open('friendly_numbers.txt', 'r', encoding='utf-8') as numbers_file:
                numbers_content = numbers_file.read()

            # Insert the contents into the Text widget
            #numbers_text.config(state=NORMAL)
            numbers_text.insert(END, numbers_content)
            #numbers_text.config(state=DISABLED)
        except FileNotFoundError:
            #numbers_text.config(state=NORMAL)
            numbers_text.insert(END, "شماره‌ها یافت نشدند.")
            #numbers_text.config(state=DISABLED)
        
        #________________________________
        def save_friendly_numbers():
            try:
                # Get the contents of the Text widget
                numbers_content = numbers_text.get("1.0", END)

                # Write the contents to the friendly_numbers.txt file
                with open('friendly_numbers.txt', 'w', encoding='utf-8') as numbers_file:
                    numbers_file.write(numbers_content)

                # Show a message indicating successful saving
                messagebox.showinfo("Friendly Numbers Saved", "Friendly numbers saved successfully to: friendly_numbers.txt", master=friendly_numbers_window)
            except Exception as e:
                # Show an error message if there's an issue saving
                messagebox.showerror("Error", f"Error saving friendly numbers: {e}", master=friendly_numbers_window)

        save_button = Button(friendly_numbers_window, text='ذخیره', bg='#282a36', fg='white', command=save_friendly_numbers, font=('b nazanin', 12))
        save_button.place(x=120, y=255)
        save_button.bind('<Enter>', onhover)
        save_button.bind('<Leave>', onleave)

        friendly_numbers_window.wait_window()

    friendly_numbers_button = Button(advanced_settings_window, text='شماره دوستان', bg='#282a36', fg='white', command=open_friendly_numbers_window, font=('b nazanin', 14))
    friendly_numbers_button.place(x=310, y=20)
    friendly_numbers_button.bind('<Enter>', onhover)
    friendly_numbers_button.bind('<Leave>', onleave)

    
    # Entry for friendly message
    friendly_message_label = Label(advanced_settings_window, text='متن پیام دوستانه :', bg='#37948c', font=('b nazanin', 15))
    friendly_message_label.place(x=10, y=120)
    #-------------------------------------------------

    friendly_message_entry = Text(advanced_settings_window, wrap="word", height=16, width=25, font=('b nazanin', 12), state=NORMAL)
    friendly_message_entry.place(x=40, y=160,height=300,width=300)

        # Create a Scrollbar for the Text widget
    scrollbar = Scrollbar(advanced_settings_window, command=friendly_message_entry.yview)
    scrollbar.place(x=341,y=160, height=300,width=20)

    # Link the Scrollbar to the Text widget
    friendly_message_entry.config(yscrollcommand=scrollbar.set)

    try:
        # Read the contents of numbers.txt
        with open('friendly_msg.txt', 'r', encoding='utf-8') as friendly_msg_file:
            msg_content = friendly_msg_file.read()

        # Insert the contents into the Text widget
        #numbers_text.config(state=NORMAL)
        friendly_message_entry.insert(END, msg_content)
        #numbers_text.config(state=DISABLED)
    except FileNotFoundError:
        #numbers_text.config(state=NORMAL)
        friendly_message_entry.insert(END, "پیامی یافت نشد.")
        #numbers_text.config(state=DISABLED)

    #--------------------
    
    # Checkbox for sending messages based on name or number
    #send_based_on_name_var = IntVar()
    send_based_on_name_checkbox = Checkbutton(advanced_settings_window, text='ارسال پیام بر اساس اسم یا شماره', variable=send_based_on_name_var, bg='#37948c', font=('b nazanin', 15))
    send_based_on_name_checkbox.place(x=10, y=50)
    
    advanced_settings_entry_label = Label(advanced_settings_window,
        text='ارسال          پیام به دوستان بعد از         پیام',
        bg='#37948c', font=('b nazanin', 15))
    advanced_settings_entry_label.place(x=10, y=90)
    
    advanced_settings_entry1 = Entry(advanced_settings_window, font=('b nazanin', 12))
    advanced_settings_entry1.place(x=41, y=95,width=37)

    advanced_settings_entry2 = Entry(advanced_settings_window, font=('b nazanin', 12))
    advanced_settings_entry2.place(x=216, y=95,width=37)
    
    


    save_button = Button(advanced_settings_window, text='ذخیره تنظیمات', bg='#282a36', fg='white', command=save_advanced_settings, font=('b nazanin', 14, 'bold'))
    save_button.place(x=310, y=80)
    save_button.bind('<Enter>', onhover)
    save_button.bind('<Leave>', onleave)

   


    
    load_advanced_settings()
    
    advanced_settings_window.wait_window()


def save_settings(delay, include_signature, include_gregorian, include_jalali, include_random_emoji, include_text_only, number_prefix):
    global delay_value, signature_var, gregorian_var, jalali_var, random_emoji_var, number_prefix_var, include_text_only_var
    if include_text_only_var.get()==1:
      delete_image_path   
    try:
        with open('settings.txt', 'w', encoding='utf-8') as settings_file:
            settings_file.write(f'delay={delay}\n')
            settings_file.write(f'include_signature={include_signature}\n')
            settings_file.write(f'include_gregorian={include_gregorian}\n')
            settings_file.write(f'include_jalali={include_jalali}\n')
            settings_file.write(f'include_random_emoji={include_random_emoji}\n')
            settings_file.write(f'include_text_only={include_text_only}\n')  # Save the state of the checkbox
            settings_file.write(f'number_prefix={number_prefix}\n')
        print("Settings saved.")
    except Exception as e:
        print(f'Error saving settings: {e}')


def load_settings():
    global delay_value, signature_var, gregorian_var, jalali_var, random_emoji_var, number_prefix_var, include_text_only_var
    
    try:
        with open('settings.txt', 'r', encoding='utf-8') as settings_file:
            settings = settings_file.readlines()

        for setting in settings:
            key, value = setting.strip().split('=')
            if key == 'delay':
                delay_value.set(int(value))
            elif key == 'include_signature':
                signature_var.set(int(value.lower()))
            elif key == 'include_gregorian':
                gregorian_var.set(int(value.lower()))
            elif key == 'include_jalali':
                jalali_var.set(int(value.lower()))
            elif key == 'include_random_emoji':
                random_emoji_var.set(int(value.lower()))
            elif key == 'include_text_only':
                include_text_only_var.set(int(value.lower()))  # Set the state of the checkbox
            elif key == 'number_prefix':
                number_prefix_var.set(value)
        # delete the image place
        if include_text_only_var.get()==1:
            delete_image_path()
        
        print("Settings loaded.")
    except FileNotFoundError:
        print("Settings file not found.")
    except Exception as e:
        print(f'Error loading settings: {e}')



def save_advanced_settings():
    global  enable_advanced_var,enable_advanced_checkbox,send_based_on_name_var,send_based_on_name_checkbox,advanced_settings_entry1,advanced_settings_entry2,friendly_message_entry
    try:
        # Save advanced settings to a file or use as needed
        with open(get_full_path('advanced_settings.txt'), 'w', encoding='utf-8') as advanced_file:
            advanced_file.write(f'Enable Advanced: {enable_advanced_var.get()}\n')
            advanced_file.write(f'Based on Name or Number: {send_based_on_name_var.get()}\n')
            advanced_file.write(f'Send {advanced_settings_entry2.get()} Friendly messages after {advanced_settings_entry1.get()} messages\n')

        # Save friendly message content to friendly_msg.txt
        try:
            with open('friendly_msg.txt', 'w', encoding='utf-8') as friendly_msg_file:
                friendly_msg_file.write(friendly_message_entry.get("1.0", END))
        except Exception as e:
            messagebox.showerror("Error", f"Error saving friendly message: {e}")

        messagebox.showinfo("Advanced Settings Saved", "تنظیمات پیشرفته ذخیره شد")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving advanced settings: {e}")
enable_advanced_var = IntVar()  # Assuming it's an IntVar; adjust accordingly


send_based_on_name_var = IntVar()

friendly_message_var = StringVar()



def load_advanced_settings():
    global  enable_advanced_var,enable_advanced_checkbox,send_based_on_name_var,send_based_on_name_checkbox,advanced_settings_entry1,advanced_settings_entry2,friendly_message_entry
    try:
        with open('advanced_settings.txt', 'r', encoding='utf-8') as advanced_file:
            settings = advanced_file.readlines()

        for setting in settings:
            # Ensure that split(': ') produces the expected number of elements
            key_value = setting.strip().split(': ')
            if len(key_value) == 2:
                key, value = key_value
                if key == 'Enable Advanced':
                    enable_advanced_var.set(int(value))
                    if value == '1':
                        enable_advanced_checkbox.select()

                elif key == 'Based on Name or Number':
                    send_based_on_name_var.set(int(value))
                    if value == '1':
                        send_based_on_name_checkbox.select()

            elif len(key_value) == 1 and key_value[0].startswith('Send'):
                # Handle the case where 'Send' is in the key but no colon (':') is present
                parts = key_value[0].split()
                if len(parts) == 7 and parts[1].isdigit() and parts[5].isdigit():
                    # Update the Entry widgets directly
                    advanced_settings_entry1.delete(0, END)
                    advanced_settings_entry1.insert(0, parts[5])

                    advanced_settings_entry2.delete(0, END)
                    advanced_settings_entry2.insert(0, parts[1])

        

        print("Advanced settings loaded.")
    except FileNotFoundError:
        print("Advanced settings file not found.")
    except Exception as e:
        print(f'Error loading advanced settings: {e}')

def init_advanced_settings_vars():
    global  enable_advanced_var, enable_advanced_checkbox, send_based_on_name_var, send_based_on_name_checkbox, advanced_settings_entry1, advanced_settings_entry2, friendly_message_entry
    global  advanced_settings_entry1_value,advanced_settings_entry2_value
    # Initialize the variables
    enable_advanced_var = IntVar()
    send_based_on_name_var = IntVar()

    try:
        with open('advanced_settings.txt', 'r', encoding='utf-8') as advanced_file:
            settings = advanced_file.readlines()

        for setting in settings:
            key_value = setting.strip().split(': ')
            if len(key_value) == 2:
                key, value = key_value
                if key == 'Enable Advanced':
                    enable_advanced_var.set(int(value))
                   # print('done')

                elif key == 'Based on Name or Number':
                    send_based_on_name_var.set(int(value))

            elif len(key_value) == 1 and key_value[0].startswith('Send'):
                parts = key_value[0].split()
                if len(parts) == 7 and parts[1].isdigit() and parts[5].isdigit():
                    advanced_settings_entry1_value = int(parts[5])
                    advanced_settings_entry2_value = int(parts[1])

        # Initialize other variables if needed

        #print2console("Advanced settings variables initialized.")
    except FileNotFoundError:
        print2console("تنظیمات پیشرفته یافت نشد", lang='fa')
    except Exception as e:
        print2console(f'Error initializing advanced settings variables: {e}', lang='en')

# Call this function to initialize the variables without opening the window



entAry= Entry(root, width=50)


button=Button(root,height=1,width=14,text='بارگذاری شماره',bg='#282a36',fg='white', border=0,command=open_input_window,font=('b nazanin',12))
button.place(x=10,y=0)
button.bind('<Enter>', onhover)
button.bind('<Leave>', onleave)

counter_sent=0
remaining_label = Label(root, text=f" شماره‌های باقی‌مانده:  {remaining_numbers}", bg='#282a36', fg='white',font=('b nazanin',12))
remaining_label.place(x=10, y=52)
sent_label = Label(root, text=f" شماره‌های ارسال‌شده:  {counter_sent}", bg='#282a36', fg='white',font=('b nazanin',12))
sent_label.place(x=190, y=52)

save_csv_button = Button(root, text='ذخیره گزارش', command=save_to_csv, bg='#282a36', fg='white', border=0,font=('b nazanin',12))
save_csv_button.place(x=390, y=50)
save_csv_button.bind('<Enter>', onhover1)
save_csv_button.bind('<Leave>', onleave)


button=Button(root,height=1,width=14,text='انتخاب متن',bg='#282a36',fg='white', border=0,command=open_input_window1,font=('b nazanin',12))
button.place(x=170,y=0)
button.bind('<Enter>', onhover)
button.bind('<Leave>', onleave)
button=Button(root,height=1,width=14,text='انتخاب تصویر',bg='#282a36',fg='white', border=0, command=select_image,font=('b nazanin',12))
button.place(x=330,y=0)
button.bind('<Enter>', onhover)
button.bind('<Leave>', onleave)
button=Button(root,height=1,width=14,text='ارسال',bg='#282a36',fg='white', border=0, command=start_sending_messages,font=('b nazanin',12))
button.place(x=490,y=0)
button.bind('<Enter>', onhover)
button.bind('<Leave>', onleave)
button=Button(root,height=1,width=14,text='توقف ارسال',bg='#282a36',fg='white', border=0, command=stop_sending_messages, font=('b nazanin',12))
button.place(x=650,y=0)
button.bind('<Enter>', onhover)
button.bind('<Leave>', onleave)
settings_button = Button(root, height=1, width=14, text='تنظیمات', bg='#282a36', fg='white', border=0, command=open_settings_window, font=('b nazanin', 12))
settings_button.place(x=650, y=50)
settings_button.bind('<Enter>', onhover)
settings_button.bind('<Leave>', onleave)

open_browser_button = Button(root,height=1, width=14, text='ارتباط با واتساپ', bg='#282a36', fg='white', border=0, command=open_browser, font=('b nazanin', 12))
open_browser_button.place(x=490, y=50)
open_browser_button.bind('<Enter>', onhover)
open_browser_button.bind('<Leave>', onleave)

# Create a Text widget for console output
console_output = Text(root, wrap="word", height=10, width=94, border=3,state=DISABLED)
console_output.place(x=10, y=100, height=245)

# Create a Scrollbar for the Text widget
scrollbar = Scrollbar(root, border=2,command=console_output.yview)
scrollbar.place(x=768, y=100, height=245)  # Adjust the position and height as needed


# Link the Scrollbar to the Text widget
console_output.config(yscrollcommand=scrollbar.set)
# Apply the font to the tagged region

# Configure a tag for custom font, alignment, and direction
console_output.tag_configure('custom_font', font=('Times New Roman', 12, 'bold'))
console_output.tag_configure('custom_align', justify=LEFT)
console_output.tag_configure('ltr', justify=LEFT)
console_output.tag_configure('rtl', justify=RIGHT)
# Example usage
print2console("This text is right-aligned.", lang='en')
print2console("Another right-aligned text.", lang='en')
print2console("این متن راست چین است.", lang='fa')



root.mainloop()



    