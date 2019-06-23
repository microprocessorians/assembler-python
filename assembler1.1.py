##no negative made for imm

def branches(value,size):
    mask = 1 << size-1
    number=''
    for i in range(1,size+1):
        if value & mask:
            number += '1'
        else:
            number += '0'
        value <<= 1
    return number
def register(string,line):
    if string[0] != 'r':
        print('wrong register name in line ',line)
    else:
        try:
            number = bin(int(string[1:]))[2:].zfill(4)
        except:
            print('wrong register name in line ',line)
        else:
            if int(number,2)>15:
                print('wrong register number in line ',line)
            else:
                return number
def immediate(string,line,size):
    if string[-1].isdigit():
        number = string
        try:
            number=bin(int(number))[2:].zfill(size)
        except:
            print('immediate value entered is wrong in line ',line)
        else:
            if int(number,2)>((2**size)-1):
                print('immediate value exceeded value in line ',line)
            else:
                return number
    elif string[-1] == 'h':
        number = string[:-1]
        try:
            number = bin(int(number,16))[2:].zfill(size)
        except:
            print('immediate value entered is wrong in line ',line)
        else:
            if int(number,2)>((2**size)-1):
                print('wrong register number in line ',line)
            else:
                return number
    elif string[-1] == 'b':
        number = string[:-1]
        try:
            number = number.zfill(size)
        except:
            print('immediate value entered is wrong in line ',line)
        else:
            if int(number,2)>((2**size)-1):
                print('wrong register number in line ',line)
            else:
                return number

################fetching data from text file###############################################
try:
    file = open(r'C:\Users\ahmed\Desktop\learn python\assembly1.txt')
    assembly = file.readlines()
    file.close()
except:
    print('file not found') 
###########################################################################################
else:
    #############remove beginnig spaces and tabs and endlines and numbers the lines######### 
    line_counter=1
    assembly2=[]
    for (line_counter,line) in enumerate(assembly):
        line_counter += 1
        line=line.strip()
        if line != '':
            if line != '\n' and line[0]!=';':
                assembly2.append([line,line_counter])
                if line.find(';') != -1:
                    assembly2[-1]=[line[:line.find(';')],line_counter]
                assembly2[-1][0]=assembly2[-1][0].rstrip()      
    assembly = assembly2
    line_counter = 0##delete
    assembly2 = 0##delete
    #############remove line comments##################
    #####now assembly is a list of lists each list contains string of line of code and index
    #####in original written assembly#######################################################

#################collecting labels##########################################################
    labels={}
    for (line_counter,line) in enumerate(assembly):
        place = line[0].find(':')
        label = line[0][:place].rstrip()
        if place != -1:
            if label in labels:
                print('error in line '+str(assembly[line_counter][1]))
                print('label used before')
            else:
                labels[label]= line_counter
                assembly[line_counter][0] = line[0][place+1:]
    line_counter=0
############################################################################################
###############assembly has pure code labels has lables and places







#####flag = 0 means wit for no regs or imm
#####flag = 1 means wait for imm
#####flag = 2 means wait for reg
    ###flag = 3 means store
    bin_file=[]
    for (line_counter,line) in enumerate(assembly):
        if line[0] == 'nop':
            bin_file.append('1'+'0'*31)
            flag=0
        elif line[0] == 'halt':
            bin_file.append('001111'+'0'*26)
            flag=0
        elif line[0] == 'ret':
            bin_file.append('010010'+'0'*26)
            flag=0
        elif line[0][:5] == 'call ':
            bin_file.append('010001')
            flag=1
        elif line[0:5] == 'jump ':
            bin_file.append('010000')
            flag=1
        elif line[0][:5] == 'push ':
            bin_file.append('101101'+'0'*4)
            flag=2
            line[0]=line[0][4:].strip()
        elif line[0][:4] == 'pop ':
            bin_file.append('101110'+'0'*4)
            flag=2
            line[0]=line[0][3:].strip()
        elif '+' in line[0]:
            if '[' in line[0]:
                if line[0].find('[') < line[0].find('='):
                    flag=3
                    bin_file.append('101011')#store
                    reg = line[0][1:line[0].find('+')].strip()
                    bin_file[-1] = bin_file[-1] + register(reg,line[1])
                    reg = line[0][line[0].find('r',2):]
                    bin_file[-1] = bin_file[-1] + register(reg,line[1])
                    imm = line[0][line[0].find('+')+1:line[0].find(']')].strip()
                    bin_file[-1] = bin_file[-1] + immediate(imm,line[1],18)
                else:
                    flag=3
                    bin_file.append('101100')#load
                    reg = line[0][line[0].find('[')+1:line[0].find('+')].strip()
                    bin_file[-1] = bin_file[-1] + register(reg,line[1])
                    reg = line[0][:line[0].find('=')].strip()
                    bin_file[-1] = bin_file[-1] + register(reg,line[1])
                    imm=line[0][line[0].find('+')+1:line[0].find(']')].strip()
                    bin_file[-1] = bin_file[-1] + immediate(imm,line[1],18)
            else:
                if '+=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0'*4
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100000')
                elif line[0].find('=') < line[0].find('+'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0'*4 + '+'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100000')
                        func = '+'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif '-' in line[0]:
                if '-=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0'*3 + '1'
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100001')
                elif line[0].find('=') < line[0].find('-'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0'*3 +'1'+ '-'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100001')
                        func = '-'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif '&' in line[0]:
                if '&=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0100'
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100100')
                elif line[0].find('=') < line[0].find('&'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0100&'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100100')
                        func = '&'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif '|' in line[0]:
                if '|=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0101'
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100101')
                elif line[0].find('=') < line[0].find('|'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0101|'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100101')
                        func = '|'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif '^' in line[0]:
                if '^=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0101'
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100110')
                elif line[0].find('=') < line[0].find('^'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0101^'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100110')
                        func = '^'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif '#' in line[0]:
                if '#=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0111'
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100111')
                elif line[0].find('=') < line[0].find('#'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0111#'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100111')
                        func = '#'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif '*' in line[0]:
                if '*=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0010'
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100010')
                elif line[0].find('=') < line[0].find('*'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0010*'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100010')
                        func = '*'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif '$' in line[0]:
                if '$=' in line[0]:
                    if line[0].count('r') == 2:
                        flag=4# augmented regs
                        func = '0011'
                    else:
                        flag = 6#1 regs 1 imm
                        bin_file.append('100011')
                elif line[0].find('=') < line[0].find('$'):
                    if line[0].count('r') == 3:
                        flag=5#3 regs
                        func = '0011$'
                    else:
                        flag = 7#2 regs 1 imm
                        bin_file.append('100011')
                        func = '$'
                else:
                    print("error opcode can't be determined in line ",line[1])
        elif line[0][:4] == 'out ':
            flag=3
            bin_file.append('110100')
            reg = line[0][3:].strip()
            bin_file[-1] += (register(reg,line[1]) + '0'*22)
        elif line[0][:3] == 'in ':
            flag=3
            bin_file.append('001011'+'0'*8)
            reg = line[0][2:].strip()
            bin_file[-1] += (register(reg,line[1]) + '0'*14)
        elif '<' in line[0]:
            bin_file.append('101000')
            flag=8
            func = '<'
        elif line[0].count('>') == 2:
            bin_file.append('101001')
            func = '>'
            flag = 8
        elif line[0].count('>') == 3:
            bin_file.append('101010')
            func = '>'
            flag = 8
        elif line[0][:3] == 'be ':
            bin_file.append('110000')
            flag = 9
            line[0]=line[0][2:].strip()
        elif line[0][:4] == 'bne ':
            bin_file.append('110001')
            flag = 9
            line[0]=line[0][3:].strip()
        elif line[0][:4] == 'bge ':
            bin_file.append('100011')
            flag = 9
            line[0]=line[0][3:].strip()
        elif line[0][:3] == 'bg ':
            bin_file.append('110010')
            flag = 9
            line[0]=line[0][2:].strip()
        else:
            print("error opcode can't be determined in line ",line[1])
        if flag == 1:
            line[0]=line[0][4:].strip()
            string = labels[line[0]]
            number = branches(string,26)
            bin_file[-1] += number
        elif flag == 2:
            if line[0][0] != 'r':
                print('wrong register name in line ',line[1])
            else:
                try:
                    number = bin(int(line[0][1:]))[2:].zfill(4)
                except:
                    print('wrong register name in line ',line[1])
                else:
                    bin_file[-1] += (number + '0'*18)
        elif flag==4:
            bin_file.append('0'*6)#3 regs
            reg = line[0][:line[0].find('=')-1].strip()
            bin_file[-1] += register(reg,line[1])
            reg2 = line[0][line[0].find('=')+1:].strip()
            bin_file[-1] += (register(reg2,line[1]) + register(reg,line[1]))
            bin_file[-1] += (func+'0'*10)
        elif flag == 5:
            bin_file.append('0'*6)#3 regs
            reg = line[0][line[0].find('=')+1:line[0].find(func[-1])].strip()
            bin_file[-1] += register(reg,line[1])
            reg = line[0][line[0].find(func[-1])+1:].strip()
            bin_file[-1] += register(reg,line[1])
            reg = line[0][:line[0].find('=')].strip()
            bin_file[-1] += (register(reg,line[1])+func[:-1]+'0'*10)
        elif flag == 6:
            reg = line[0][:line[0].find('=')-1].strip()
            bin_file[-1] += (register(reg,line[1])*2)
            imm = line[0][line[0].find('=')+1:].strip()
            bin_file[-1] += immediate(imm,line[1],18)
        elif flag == 7:
            reg = line[0][line[0].find('=')+1:line[0].find(func)].strip()
            bin_file[-1] +=  register(reg,line[1])
            reg = line[0][:line[0].find('=')].strip()
            bin_file[-1] +=  register(reg,line[1])
            imm = line[0][line[0].find(func)+1:].strip()
            bin_file[-1] += immediate(imm,line[1],18)
        elif flag == 8:
            reg = line[0][line[0].rfind(func)+1:].strip()
            bin_file[-1] += register(reg,line[1])
            reg = line[0][:line[0].find(func)].strip()
            bin_file[-1] += (register(reg,line[1]) + '0'*18)
        elif flag == 9:
            reg = line[0][:line[0].find(',')].strip()
            bin_file[-1] +=  register(reg,line[1])
            line[0] = line[0][line[0].find(',')+1:].strip()
            reg = line[0][:line[0].find(',')].strip()
            bin_file[-1] +=  register(reg,line[1])
            line[0] = line[0][line[0].find(',')+1:].strip()
            try:
                imm = branches(labels[line[0]]-line_counter,18)
            except:
                print('error: label not found in line ',line[1])
            else:
                bin_file[-1] +=  imm
    out_file = open(r'binfile.txt','w')
    for binary in bin_file:
        print('"'+binary+'",',end='\n')
        out_file.write('"'+binary+'",\n')
    out_file.close()
