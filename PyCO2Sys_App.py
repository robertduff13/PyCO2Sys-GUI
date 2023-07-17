from tkinter import *
import PyCO2SYS as pyc02
import pandas as pd
import openpyxl as px
from datetime import datetime

# ----- Instructions -----
# 1. Initialize the program
# 2. Select TWO parameters for which you have known values, then click "Next"
# 3. Input the measured values for the parameters, the initial fluid conditions, and all associated errors
# 4. Once fully and correctly inputted, click "Next" or if you need to change your parameters, click "Back" and repeat Step 2
# 5. Select your desired constant sets from each dropdown for H2CO3, HSO4-, Total Borate, and HF
# 6. Once all constant sets are selected, click "Get Results" to get results or click "Back" to edit input values
# 7. Results are presented in the form "Parameter Name: Parameter Value ± Error Value"
# 8. Results are cleared and replaced anytime the "Get Results" button is pressed but can be manually cleared using the "Clear Results" button
# 9. Inputs are locked for editing once the "Next" buttons are pressed and "Back" buttons must be pressed to edit earlier inputs/selections
# 10. Enjoy!

def checkmax(bar, var):
    # called after the intvar is changed
    def _check():
        if var.get():  # checked
            if bar.numpicks < bar.maxpicks:
                bar.numpicks += 1
            else:
                var.set(0)
        else:             # unchecked
            bar.numpicks -= 1
    return _check

# ----- Create custom checkbar -----
class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], maxpicks=2, side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.maxpicks = maxpicks
      self.numpicks = 0
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var,
                           command=checkmax(self, var))
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)


   def state(self):
        return map((lambda var: var.get()), self.vars)


if __name__ == '__main__':
    # Initialise external window
    root = Tk()
    root.geometry('900x900'), root.title('CO2Sys Program')

    # Create 4 widget canvases
    canvas1 = Canvas(root, width=300, height=150, relief='solid')
    canvas1.pack()

    canvas2 = Canvas(root, width=650, height=150, relief='solid')
    canvas2.pack()

    canvas3 = Canvas(root, width=600, height=200, relief='solid')
    canvas3.pack()

    canvas4 = Canvas(root, width=300, height=300, relief='solid')
    canvas4.pack()

    canvas5 = Canvas(root, width=600, height=25, relief='solid')
    canvas5.pack()

    lbl1 = Label(root, text = 'Select input parameters:')    # Create label
    lbl1.config(font=('Segoe UI', 14)), canvas1.create_window(150, 25, window=lbl1)

    pars = ['Total Alkalinity (μmol·kg−1)', 'DIC (μmol·kg−1)', 'pH', 'pCO2 (μatm)']    # Checkbox options

    lng = Checkbar(root, pars, 2)    # Create a checkbar
    lng.pack(side=TOP, fill=X), lng.config(relief=GROOVE, bd=2)    # Place checkbar and align top, horizontal with border
    canvas1.create_window(150, 70, window=lng)    # Place checkbar at x,y

    # ----- Create a popup window with instructions on how to use the program -----
    def inst():
        puw = Toplevel()    # puw = pop up window
        puw.wm_title("CO2Sys Instructions")

        lbl_inst = Label(puw, text='----- Instructions ----- \n \
                         \n1. Initialize the program \n \
                         \n2. Select TWO parameters for which you have known values, then click "Next" \n \
                         \n3. Input the measured values for the parameters, the initial fluid conditions, and all associated errors \n \
                         \n4. Once fully and correctly inputted, click "Next" or if you need to change your parameters, click "Back" and repeat Step 2 \n \
                         \n5. Select your desired constant sets from each dropdown for H2CO3, HSO4-, Total Borate, and HF \n \
                         \n6. Once all constant sets are selected, click "Get Results" to get results or click "Back" to edit input values \n \
                         \n7. Results are presented in the form "Parameter Name: Parameter Value ± Error Value" \n \
                         \n8. Results are cleared and replaced anytime the "Get Results" button is pressed but can be manually cleared using the "Clear Results" button \n \
                         \n9. Inputs are locked for editing once the "Next" buttons are pressed and "Back" buttons must be pressed to edit earlier inputs/selections \n \
                         \n10. Enjoy! \n')
        
        lbl_inst.grid(row=0, column=0)
        
        leave = Button(puw, text='Okay', command=puw.destroy)
        leave.grid(row=1, column=0)

    # ----- Initialise a section for inputting parameters and initial conditions -----
    def par_input():
        # Clear/reset section
        canvas3.delete('all'), canvas4.delete('all')
        next.config(state=DISABLED)

        boxes_checked = [i for i in range(4) if list(lng.state())[i] == 1]    # List of checked box indexes
        boxes_unchecked = [j for j in range(4) if list(lng.state())[j] == 0]    # List of unchecked box indexes
        
        pars_unslctd = [pars[boxes_unchecked[0]], pars[boxes_unchecked[1]]]    # Parameters not selected

        if len(boxes_checked) < 2:
            canvas2.delete('all')    # Clear the canvas

            lbl2 = Label(root, text='Please Select Two Parameters')    # Create label
            lbl2.config(font=('Segoe UI', 16))    # Label font/size
            canvas2.create_window(300, 25, window=lbl2)    # Place label at x,y
        
        else:
            canvas2.delete('all')    # Clear the canvas

            pars_slctd = [pars[boxes_checked[0]], pars[boxes_checked[1]]]    # Parameters selected
            par1_type, par2_type = boxes_checked[0] + 1, boxes_checked[1] + 1    # Parameter code

            # ----- Parameter/Conditions Input (Labels, Entry Boxes) -----
            lbl2 = Label(root, text='Input Parameter Values')
            lbl2.config(font=('Segoe UI', 14)), canvas2.create_window(50, 0, window=lbl2)

            lbl3 = Label(root, text=f'Measured {pars_slctd[0]} Value:')
            lbl3.config(font=('Segoe UI', 10)), canvas2.create_window(50, 25, window=lbl3)

            entry1 = Entry(root, width=20) 
            canvas2.create_window(20, 50, window=entry1)

            lbl15 = Label(root, text='±')
            lbl15.config(font=('Segoe UI', 10)), canvas2.create_window(90, 50, window=lbl15)

            entry6 = Entry(root, width=6) 
            canvas2.create_window(120, 50, window=entry6)

            lbl4 = Label(root, text=f'Measured {pars_slctd[1]} Value:')
            lbl4.config(font=('Segoe UI', 10)), canvas2.create_window(50, 75, window=lbl4)

            entry2 = Entry(root, width=20)
            canvas2.create_window(20, 100, window=entry2)

            lbl16 = Label(root, text='±')
            lbl16.config(font=('Segoe UI', 10)), canvas2.create_window(90, 100, window=lbl16)

            entry7 = Entry(root, width=6) 
            canvas2.create_window(120, 100, window=entry7)

            lbl11 = Label(root, text='Input Initial Conditions')
            lbl11.config(font=('Segoe UI', 14)), canvas2.create_window(425, 0, window=lbl11)

            lbl12 = Label(root, text='Salinity:')
            lbl12.config(font=('Segoe UI', 10)), canvas2.create_window(275, 25, window=lbl12)

            entry3 = Entry(root, width=12) 
            canvas2.create_window(250, 50, window=entry3)

            lbl17 = Label(root, text='±')
            lbl17.config(font=('Segoe UI', 10)), canvas2.create_window(295, 50, window=lbl17)

            entry8 = Entry(root, width=6) 
            canvas2.create_window(325, 50, window=entry8)

            lbl13 = Label(root, text='Temperature (oC):')
            lbl13.config(font=('Segoe UI', 10)), canvas2.create_window(450, 25, window=lbl13)

            entry4 = Entry(root, width=12)
            canvas2.create_window(415, 50, window=entry4)

            lbl18 = Label(root, text='±')
            lbl18.config(font=('Segoe UI', 10)), canvas2.create_window(460, 50, window=lbl18)

            entry9 = Entry(root, width=6) 
            canvas2.create_window(490, 50, window=entry9)

            lbl14 = Label(root, text='Pressure (dbar):')
            lbl14.config(font=('Segoe UI', 10)), canvas2.create_window(605, 25, window=lbl14)

            entry5 = Entry(root, width=12)
            canvas2.create_window(575, 50, window=entry5)

            lbl19 = Label(root, text='±')
            lbl19.config(font=('Segoe UI', 10)), canvas2.create_window(625, 50, window=lbl19)

            entry10 = Entry(root, width=6) 
            canvas2.create_window(655, 50, window=entry10)

            # ----- Return to Parameter Selection (Clear else) -----
            def back_1():
                canvas2.delete('all'), canvas3.delete('all'), canvas4.delete('all')
                next.config(state=NORMAL)

            # ----- Constant Sets Selection (Labels, Dropdown Lists)-----
            def consts():
                canvas4.delete('all')
                next_consts.config(state=DISABLED), back1.config(state=DISABLED)

                entries = [entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(),
                           entry6.get(), entry7.get(), entry8.get(), entry9.get(), entry10.get()]
                char_remove = ["."]
                entry_is_num = []
                
                # ----- Remove decimals from inputs to check if all numeric -----
                for x in char_remove:
                    for i in range(10):
                        entry_is_num.append(entries[i].replace(x, ""))

                # ----- Check if any inputs are empty -----
                if len([i for i in range(10) if entries[i].replace(" ", "") == '']) != 0:
                    canvas3.delete('all')

                    lbl15 = Label(root, text='\n    Parameter, initial condition, and/or error values are missing    \n', relief='solid')    # Create label
                    lbl15.config(font=('Segoe UI', 16)), canvas3.create_window(300, 100, window=lbl15)    # Place label at x,y

                # ----- Check if all inputs are numeric -----
                elif len([k for k in range(10) if entry_is_num[k].isnumeric() != True]) != 0:
                    canvas3.delete('all')

                    lbl15 = Label(root, text='\n    One or more inputs is non-numeric    \n', relief='solid')    # Create label
                    lbl15.config(font=('Segoe UI', 16)), canvas3.create_window(300, 100, window=lbl15)    # Place label at x,y
            
                else:
                    canvas3.delete('all')   # Clear previous selections

                    # ----- Disable editing inputs -----
                    entry_bxs = [entry1, entry2, entry3, entry4, entry5, entry6, entry7, entry8, entry9, entry10]
                    for i in range(10):
                        entry_bxs[i].config(state=DISABLED)
                    # ----------------------------------

                    # ----- Constant Sets -----
                    k_carbonic_opts = ['Roy et al. (1993)', 'Goyet & Poisson (1989)', 'Hansson (1973) refit by Dickson & Millero (1987)', 
                                        'Mehrbach et al. (1973) refit by Dickson & Millero (1987)', 
                                        'Hansson & Mehrbach refit by Dickson & Millero (1987)', 
                                        'GEOSECS constants (NBS scale) from Mehrbach et al. (1973)', 
                                        'Constants from Peng et al. (NBS scale) from Mehrbach et al. (1973)', 
                                        'Millero (1979)', 'Cai & Wang (1998)', 'Lueker et al. (2000)', 'Mojica Prieto & Millero (2002)', 
                                        'Millero et al. (2002)', 'Millero et al. (2006)', 'Millero (2010)', 'Waters et al. (2014)', 
                                        'Sulphis et al. (2020)', 'Schockman & Byrne (2021)']
                    k_bisulphate_opts = ['Dickson (1990)', 'Khoo et al. (1977)', 'Waters & Millero (2013) / Waters et al. (2014)']
                    tot_borate_opts = ['Uppström (1974)', 'Lee et al. (2010)', 'Kuliński et al. (2018)']
                    k_fluoride_opts = ['Dickson & Riley (1979)', 'Perez & Fraga (1987)']

                    # ----- Assign default values -----
                    k_H2CO3_var = StringVar(root)
                    k_H2CO3_var.set(k_carbonic_opts[-2])

                    k_HSO4_var = StringVar(root)
                    k_HSO4_var.set(k_bisulphate_opts[0])
                    
                    tot_borate_var = StringVar(root)
                    tot_borate_var.set(tot_borate_opts[0])

                    k_HF_var = StringVar(root)
                    k_HF_var.set(k_fluoride_opts[0])

                    # ----- Labels, Dropdown Menus -----
                    lbl5 = Label(root, text='Select Eq. Constant Sets (K1, K2)')
                    lbl5.config(font=('Segoe UI', 12)), canvas3.create_window(300, 25, window=lbl5)

                    lbl6 = Label(root, text='H2CO3 (Default: Sulphis et al., 2020)')
                    lbl6.config(font=('Segoe UI', 10)), canvas3.create_window(100, 55, window=lbl6)

                    k_carbonic_drpdwn = OptionMenu(root, k_H2CO3_var, *k_carbonic_opts)
                    canvas3.create_window(100, 85, window=k_carbonic_drpdwn)

                    lbl7 = Label(root, text=f"HSO4- (Default: Dickson, 1990)")
                    lbl7.config(font=('Segoe UI', 10)), canvas3.create_window(100, 115, window=lbl7)

                    k_bisulphate_drpdwn = OptionMenu(root, k_HSO4_var, *k_bisulphate_opts)
                    canvas3.create_window(100, 145, window=k_bisulphate_drpdwn)

                    lbl8 = Label(root, text=f"Total Borate (Default: Uppström, 1974)")
                    lbl8.config(font=('Segoe UI', 10)), canvas3.create_window(500, 55, window=lbl8)

                    tot_borate_drpdwn = OptionMenu(root, tot_borate_var, *tot_borate_opts)
                    canvas3.create_window(500, 85, window=tot_borate_drpdwn)

                    lbl9 = Label(root, text=f"HF (Default: Dickson & Riley, 1979)")
                    lbl9.config(font=('Segoe UI', 10)), canvas3.create_window(500, 115, window=lbl9)

                    k_fluoride_drpdwn = OptionMenu(root, k_HF_var, *k_fluoride_opts)
                    canvas3.create_window(500, 145, window=k_fluoride_drpdwn)

                    # ----- Return to Parameter Value Input -----
                    def back_2():
                        canvas3.delete('all'), canvas4.delete('all')
                        next_consts.config(state=NORMAL), back1.config(state=NORMAL)

                        # ----- Enable editing inputs -----
                        for i in range(10):
                            entry_bxs[i].config(state= NORMAL)                        
                        # ----------------------------------

                    # ----- CO2Sys Results (Carbonate System Parameters) -----
                    def get_vals():
                        canvas4.delete('all')   # Clear previous results
                        get_ins.config(state=DISABLED), back2.config(state=DISABLED)

                        # ----- Disable dropdowns -----
                        drpdwns = [k_carbonic_drpdwn, k_bisulphate_drpdwn, tot_borate_drpdwn, k_fluoride_drpdwn]
                        for j in range(4):
                            drpdwns[j].config(state=DISABLED)
                        #------------------------------
                        
                        par_codes = ['alkalinity', 'dic', 'pH', 'pCO2']    # Parameter codes in CO2Sys

                        # ----- Get values from user input -----
                        par1, par2, sal = entry1.get(), entry2.get(), entry3.get()
                        temp, prsr = entry4.get(), entry5.get()

                        par1_err, par2_err, sal_err = entry6.get(), entry7.get(), entry8.get()
                        temp_err, prsr_err = entry9.get(), entry10.get()

                        # ----- Convert selected constant sets into their numerical CO2Sys codes -----
                        carbonic = [i for i, j in enumerate(k_carbonic_opts) if j == k_H2CO3_var.get()][0] + 1
                        bisulphate = [i for i, j in enumerate(k_bisulphate_opts) if j == k_HSO4_var.get()][0] + 1
                        borate = [i for i, j in enumerate(tot_borate_opts) if j == tot_borate_var.get()][0] + 1
                        fluoride = [i for i, j in enumerate(k_fluoride_opts) if j == k_HF_var.get()][0] + 1

                        # ----- Call CO2Sys program -----
                        co2sys = pyc02.sys(par1, par2, par1_type, par2_type, opt_k_carbonic = carbonic, opt_k_bisulfate = bisulphate,
                                        opt_total_borate = borate, opt_k_fluoride = fluoride, salinity=sal, temperature=temp, pressure=prsr,
                                        uncertainty_into = par_codes,
                                        uncertainty_from = {'par1': par1_err, 'par2': par2_err, 'salinity': sal_err, 
                                                            'temperature': temp_err, 'pressure': prsr_err})

                        # ----- Compile and display carbonate system results -----
                        par_results = [co2sys['alkalinity'], co2sys['dic'], co2sys['pH'], co2sys['pCO2']]

                        lbl10 = Label(root, text=f'\n    {pars_slctd[0]}: {co2sys[par_codes[boxes_checked[0]]]} ± {entry6.get()}\
                                    \n    {pars_slctd[1]}: {co2sys[par_codes[boxes_checked[1]]]} ± {entry7.get()} \
                                    \n    {pars_unslctd[0]}: {co2sys[par_codes[boxes_unchecked[0]]]} ± {co2sys["u_" + par_codes[boxes_unchecked[0]]]}\
                                    \n    {pars_unslctd[1]}: {co2sys[par_codes[boxes_unchecked[1]]]} ± {co2sys["u_" + par_codes[boxes_unchecked[1]]]}\
                                    \n', justify='left', relief='solid')
                        lbl10.config(font=('Segoe UI', 10)), canvas4.create_window(150, 75, window = lbl10)

                        # ----- Initialise results history Excel workbook and insert results and time -----
                        res_hist_path = 'PyCO2Sys_Result_History.xlsx'
                        wb = px.load_workbook(res_hist_path)
                        page = wb.active
                        page.insert_rows(4,1)
                        page['A4'], page['B4'], page['C4'] = datetime.now(), par_results[0], par_results[1]
                        page['D4'], page['E4'] = par_results[2], par_results[3]
                        # ---------------------------------------------------------------------------------

                        # ----- Input error values into worksheet -----
                        page['G4'], page['H4'] = co2sys['u_alkalinity'], co2sys['u_dic']
                        page['I4'], page['J4'] = co2sys['u_pH'], co2sys['u_pCO2']
                        # ---------------------------------------------

                        # ----- Save workbook -----
                        wb.save(res_hist_path)

                        # ----- Clear results -----
                        def back_3():
                            canvas4.delete('all')
                            get_ins.config(state=NORMAL), back2.config(state=NORMAL)

                            # ----- Enable dropdowns -----
                            for j in range(4):
                                drpdwns[j].config(state=NORMAL)
                            #------------------------------

    # ----- Buttons -----
                        clr_results = Button(root, text = 'Clear Results', command = back_3, background='brown', foreground = 'white', width=10)
                        canvas4.create_window(150, 150, window = clr_results)
            
                get_ins = Button(root, text = 'Get Results', command = get_vals, background='green', foreground = 'white', width=10)
                canvas3.create_window(250, 190, window = get_ins)
                back2 = Button(root, text = 'Back', command = back_2, background='brown', foreground = 'white', width=10)
                canvas3.create_window(350, 190, window = back2)

            next_consts = Button(root, text = 'Next', command = consts, background='green', foreground = 'white', width=10)
            canvas2.create_window(250, 125, window=next_consts)
            back1 = Button(root, text = 'Back', command = back_1, background='brown', foreground = 'white', width=10)
            canvas2.create_window(350, 125, window=back1)

    next = Button(root, text = 'Next', command = par_input, background='green', foreground = 'white', width=10)
    canvas1.create_window(150, 115, window = next)

    instructions = Button(root, text='Instructions', command=inst, background='orange', width=10)
    canvas5.create_window(600, 20, window = instructions)


    # ----- Infinite loop to keep window running -----
    root.mainloop()