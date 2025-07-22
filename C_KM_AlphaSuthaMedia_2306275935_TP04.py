from tkinter import *
from tkinter import messagebox

def checkSumCalculation(number):
    k = 1 # odd - even detector
    x = 0
    for i in number:
        if k % 2 != 0:
            x += int(i)
        else:
            x += 3 * int(i)
        k += 1
    x = x % 10
    if x != 0:
        checkDigit = 10 - x
    else:
        checkDigit = x
    return checkDigit

def inputChecker(code):
    try:
        int(code)
        if len(code) < 12:
            raise Exception
        return True
    except:
        return False

class Window:
    def __init__(self):
        self.window = Tk()
        self.window.title("EAN-13 [by Alpha Sutha Media]")
        self.window.resizable(False, False)


class MainApp(Window):
    def __init__(self):
        super().__init__()
        
        window = self.window
        window.title = self.window.title()
        window.resizable = self.window.resizable()

        frameAtas = Frame(window) # Digunakan untuk label dan input user
        frameBawah = Frame(window) # Digunakan untuk mencetak Barcode
        frameAtas.pack()
        frameBawah.pack()

        # Label dan Entry untuk input user
        frameAtas1 = Frame(frameAtas) # Digunakan untuk input user save asBarcode
        frameAtas1.pack()
        labelSaveAs = Label(master = frameAtas1, text="Save barcode to PS file [eg: EAN13.eps]")
        labelSaveAs.pack()
        self.SaveAs = StringVar() 
        entrySaveAs = Entry(master = frameAtas1, textvariable=self.SaveAs)
        entrySaveAs.pack()

        # Label dan kode 12 digit untuk input user
        frameAtas2 = Frame(frameAtas) # Digunakan untuk input user save asBarcode
        frameAtas2.pack()
        labelEnterCode = Label(master = frameAtas2, text="Enter code (first 12 decimal digits):")
        labelEnterCode.pack()
        self.Code = StringVar()
        # Checker if tidak 12 digit input or bukan string 
        entryEnterCode = Entry(master = frameAtas2, textvariable=self.Code)
        entryEnterCode.pack()

        # Canvas
        self.canvas = Canvas(master=frameBawah, width=500, height=500, bg="white")
        self.canvas.pack()

        # Program eksekusi
        entryEnterCode.bind('<Return>', self.inputChecker)

        self.EAN13_Structure = {
            0 : ["LLLLLL", "RRRRRR"], 
            1 : ["LLGLGG", "RRRRRR"], 
            2 : ["LLGGLG", "RRRRRR"], 
            3 : ["LLGGGL", "RRRRRR"], 
            4 : ["LGLLGG", "RRRRRR"], 
            5 : ["LGGLLG", "RRRRRR"], 
            6 : ["LGGGLL", "RRRRRR"], 
            7 : ["LGLGLG", "RRRRRR"], 
            8 : ["LGLGGL", "RRRRRR"], 
            9 : ["LGGLGL", "RRRRRR"]
                                }
        
        self.EAN13_Encoding = {
        # Format "Digit", [L-Code, G-Code, R-Code]
            0 : ["0001101", "0100111", "1110010"], 
            1 : ["0011001", "0110011", "1100110"], 
            2 : ["0010011", "0011011", "1101100"], 
            3 : ["0111101", "0100001", "1000010"], 
            4 : ["0100011", "0011101", "1011100"], 
            5 : ["0110001", "0111001", "1001110"], 
            6 : ["0101111", "0000101", "1010000"], 
            7 : ["0111011", "0010001", "1000100"], 
            8 : ["0110111", "0001001", "1001000"], 
            9 : ["0001011", "0010111", "1110100"]
                                }
        
        window.mainloop()

    def storeEncodedkey(self):
        self.EncodedKey = list()
        # Get LGR Code for each digit
        for i in range(1, 13):

            if self.getStructure[i-1] == "L": x = 0
            elif self.getStructure[i-1] == "G": x = 1
            else: x  = 2

            self.EncodedKey.append(self.EAN13_Encoding[int(self.CodeConverted[i])][x])
        self.drawBarcode()

    def getKeyStructure(self):
        # First key is the key of EAN13_Structure
        self.getStructure = self.EAN13_Structure[int(self.idNumber[0])]
        self.getStructure = self.getStructure[0] + self.getStructure[1]
        self.CodeConverted = self.idNumber + str(self.checkDigit)
        self.storeEncodedkey()
    
    def checksum(self):
        self.checkDigit = checkSumCalculation(self.idNumber)
        self.getKeyStructure()

    def inputChecker(self, event):
        # crop the input to 12 digit
        if len(self.Code.get()) > 12:
            self.idNumber = self.Code.get()[0:12]
        else:
            self.idNumber = self.Code.get()

        if inputChecker(self.idNumber) == True:
            self.canvas.delete("all") # Clear canvas
            self.checksum()
        else:
            messagebox.showerror("Wrong input!", "Please enter correct input code.")
    
    def saving(self):
        if self.SaveAs.get().find(".eps") == -1:
            self.SaveAs.set(self.SaveAs.get() + ".eps")

        self.canvas.postscript(file=self.SaveAs.get(), colormode='color')

    def drawBarcode(self):
        # template
        self.canvas.create_text(250, 50, text="EAN-13 Barcode", font=("Arial", 20, "bold"))
        self.canvas.create_text(250, 450, text=f"Check Digit : {self.checkDigit}", font=("Arial", 20, "bold"), fill="#ffb25b")
        # Draw the barcode
        centering = 23
        
        # Draw the first guard bar
        self.canvas.create_text(centering-5, 385, text=self.CodeConverted[0], font=("Arial", 20, "bold"))
        self.canvas.create_rectangle(5+centering, 100, 9+centering, 370, fill="blue", outline="white")
        self.canvas.create_rectangle(5+5+centering, 100, 9+5+centering, 370, fill="blue", outline="white")

        x = 9+5+centering
        middleCounter = 1
        for i in self.EncodedKey:
            self.canvas.create_text(centering-15 + x , 385, text=self.CodeConverted[middleCounter], font=("Arial", 20, "bold"))
            for j in i:
                if j == "1":
                    self.canvas.create_rectangle(x, 100, x+4, 350, fill="black")
                    x += 1 
                else:
                    self.canvas.create_rectangle(x, 100, x+4, 350, fill="white", outline="white")
                    x += 1
                x += 4
            # Draw the middle guard bar
            if middleCounter == 6:
                self.canvas.create_rectangle(x, 100, x+4, 370, fill="blue", outline="white")
                self.canvas.create_rectangle(x+4, 100, x+4+4, 370, fill="blue", outline="white")
                x += 9
            middleCounter += 1

        # Draw the end guard bar
        self.canvas.create_rectangle(x, 100, x+4, 370, fill="blue", outline="white")
        self.canvas.create_rectangle(x+4, 100, x+4+4, 370, fill="blue", outline="white")

        if self.SaveAs.get() == "":
            messagebox.showinfo("Information", "Please enter the name of the barcode file.")
        else:
            self.saving()
            messagebox.showinfo("Information", "Barcode has been saved.")

def main():
    MainApp()

if __name__ == "__main__":  
    main()