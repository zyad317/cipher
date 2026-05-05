from math import ceil
import operator
import numpy as np 

def convert_to_hex(plaintext=""):
    
    if plaintext.isalpha() == True:
            conc = []
            for i in plaintext:
                plain = format(ord(i),"X")
                conc.append(plain)
            concat = "".join(conc)
            conc1 = []
            i = 0
            
            while len(conc1) != ceil(len(concat)/16):
                part = concat[i:i+16]
                if len(concat[i:i+16])<16:
                    pad_bytes = (16 - len(part)) // 2   
                    pad = format(pad_bytes, "02X") * pad_bytes
                    part += pad
                    #part = part+ ("0"+str(abs(len(plaintext) - 16)))
                if len(concat[i:i+16])<16:
                    part = part+ ("0"* (16 - len(part)))
                conc1.append(part)
                i+=16
                
            return(" ".join(conc1))
    elif plaintext.isalpha() == False:
        return(plaintext)

def convert_to_binary(x=""):
    if x.isalpha()  == False:
        binary = []
        i=0
        while i < len(x):
            if ((x[i%len(x)]).isdigit()) and ((x[(i+1)%len(x)]).isdigit()):
                binary.append(format(((ord(x[i%len(x)]) -48 )%10),"04b") + format(((ord(x[(i+1)%len(x)]) -48 )%10),"04b"))
            elif ((x[i%len(x)]).isalpha()) and ((x[(i+1)%len(x)]).isalpha()):
                binary.append(format(ord(x[i%len(x)])-55,"04b") + format(ord(x[(i+1)%len(x)])-55,"04b"))
            elif ((x[i%len(x)]).isdigit()) and ((x[(i+1)%len(x)]).isalpha()):
                binary.append((format(((ord(x[i%len(x)]) -48 )%10),"04b")) + (format(ord(x[(i+1)%len(x)])-55,"04b")))
            elif ((x[i%len(x)]).isalpha()) and ((x[(i+1)%len(x)]).isdigit()):
                binary.append(format(ord(x[i%len(x)])-55,"04b") + format(((ord(x[(i+1)%len(x)]) -48 )%10),"04b"))
            i+=2     
        return("".join(binary))
    elif x.isalpha()  == True:
        x = convert_to_hex(x)
        binary = []
        i=0
        while i < len(x):
            if ((x[i%len(x)]).isdigit()) and ((x[(i+1)%len(x)]).isdigit()):
                binary.append(format(((ord(x[i%len(x)]) -48 )%10),"04b") + format(((ord(x[(i+1)%len(x)]) -48 )%10),"04b"))
            elif ((x[i%len(x)]).isalpha()) and ((x[(i+1)%len(x)]).isalpha()):
                binary.append(format(ord(x[i%len(x)])-55,"04b") + format(ord(x[(i+1)%len(x)])-55,"04b"))
            elif ((x[i%len(x)]).isdigit()) and ((x[(i+1)%len(x)]).isalpha()):
                binary.append((format(((ord(x[i%len(x)]) -48 )%10),"04b")) + (format(ord(x[(i+1)%len(x)])-55,"04b")))
            elif ((x[i%len(x)]).isalpha()) and ((x[(i+1)%len(x)]).isdigit()):
                binary.append(format(ord(x[i%len(x)])-55,"04b") + format(((ord(x[(i+1)%len(x)]) -48 )%10),"04b"))
            i+=2     
        return("".join(binary))

def CipherEncode(mode="encode",PlainText="", KeyText=""):
    raw_key_binary = convert_to_binary(KeyText)
    textsplit = []
    i=0
    while len(textsplit) < (len(raw_key_binary)//64):
        textsplit.append(raw_key_binary[i:i+64])
        i+=64
    
    pc1= [57,49,41,33,25,17,9,1,58,50,42,34,26,
          18,10,2,59,51,43,35,27,19,11,3,60,52,44,
          36,63,55,47,39,31,23,15,7,62,54,46,38,30,
          22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
    pc1_key_bits=[]
    
    #for j in range(len(textsplit)):
    for i in pc1:
        pc1_key_bits.append(textsplit[0][i-1])
    pc1_key_string = []
    
    k=0
    while len(pc1_key_string) <= (int(len(pc1_key_bits)/56)):
        pc1_key_string.append("".join(pc1_key_bits[k:k+56]))
        k+=56
    
    left_key_half = "".join(pc1_key_string[0][:28])
    right_key_half = "".join(pc1_key_string[0][28:])
    
    
    
    LeftShift = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    left_half_schedule  = [left_key_half]
    right_half_schedule  = [right_key_half]
    for shift_amount in LeftShift:
        current_left_half = left_half_schedule[-1]
        current_right_half = right_half_schedule[-1]
        shiftC = current_left_half[shift_amount:]  + current_left_half[:shift_amount]
        shiftD = current_right_half[shift_amount:] + current_right_half[:shift_amount]
        left_half_schedule.append(shiftC)
        right_half_schedule.append(shiftD)
    #second iteration
    combined_key_halves = list(zip(left_half_schedule,right_half_schedule))
    
    pc2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
        
    subkey_bits= []
    for i1 in range(1,17):
        p = "".join(combined_key_halves[i1])
        for f in pc2:
            subkey_bits.append(p[f-1])
    all_subkeys_string = "".join(subkey_bits)
    subkey_index = 0
    subkeys = []
    while len(subkeys)!=16:
        subkeys.append(all_subkeys_string[subkey_index:subkey_index+48])
        subkey_index+=48
    
    
    plaintext_hex = convert_to_hex(PlainText)
    plaintext_nibbles = []
    for i in plaintext_hex:
        if i.isdigit():
           digit = format(((ord(i) -48 )%10),"04b")
           plaintext_nibbles.append(digit)
        elif i.isalpha():
           alpha = format(ord(i)-55,"04b")
           plaintext_nibbles.append(alpha)
    
    plaintext_binary1 = "".join(plaintext_nibbles)
    #print(len(plaintext_binary1))
    
    final = []
    for z in range(0,len(plaintext_binary1),64):
        plaintext_binary = plaintext_binary1[z:z+64]
        half_block_size = int((len(plaintext_binary)/2))
        left_plaintext = " ".join(plaintext_binary[:half_block_size])
        right_plaintext = " ".join(plaintext_binary[half_block_size:])
        
        IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,
              12,4,62,54,46,38,30,22,14,6,64,56,48,40,
              32,24,16,8,57,49,41,33,25,17,9,1,59,51,
              43,35,27,19,11,3,61,53,45,37,29,21,13,5,
              63,55,47,39,31,23,15,7]
        
        
        ip_bits=[]
        for i in IP:
            ip_bits.append(plaintext_binary[i-1])
        ip_half_size = int((len(ip_bits)/2))
        ip_left_half = "".join(ip_bits[:ip_half_size])
        ip_right_half = "".join(ip_bits[ip_half_size:])
        
        first_subkey  =subkeys[0]
        feistel_input = ip_right_half 
        
        E_BITSELECTIONTABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
        expanded_bits=[]
        for i in E_BITSELECTIONTABLE:
            expanded_bits.append(feistel_input[i-1])
        expanded_half = "".join(expanded_bits)
        
        expanded_int = int(expanded_half, 2)
        subkey_int = int(first_subkey, 2)
        xor_result = format(operator.xor(expanded_int, subkey_int), '048b')
        six_bit_groups = []
        group_index = 0 
        while len(six_bit_groups) != 8:
            six_bit_groups.append(xor_result[group_index:group_index+6])
            group_index+=6
        E_BITSELECTIONTABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
        P =[16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
        matrixS =[
        [
        14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
        0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
        4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
        15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13
        ],
            
                
        [
        15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
        3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
        0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
        13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9
        ],
        
        [
        10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
        13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
        13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
        1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12
        ],
        
        [
        7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
        13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
        10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
        3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14
        ],
        
        [
        2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
        14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
        4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
        11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3
        ],
            
        [
        12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
        10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
        9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
        4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13
        ],
        
        [
        4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
        13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
        1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
        6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12
        ],
            
        [
        13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
        1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
        7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
        2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11
        ]
        ]
        #second
        new_right_halves = []
        new_left_halves = []
        L = ip_left_half
        R = ip_right_half
        for round_number in range(16):
            expanded_bits=[]
            for v in E_BITSELECTIONTABLE:
                expanded_bits.append(R[v-1])
            expanded_half = "".join(expanded_bits)
            
            expanded_int = int(expanded_half, 2)
            subkey_int = int(subkeys[round_number], 2)
            xor_result = format(operator.xor(expanded_int, subkey_int), '048b')
            
            six_bit_groups = []
            group_index = 0 
            while len(six_bit_groups) != 8:
                six_bit_groups.append(xor_result[group_index:group_index+6])
                group_index+=6
                
            sbox_inputs  = six_bit_groups 
            sbox_outputs =[]
            for sbox_index in range(len(sbox_inputs)):
                sbox_matrix = np.array(matrixS[sbox_index][:]).reshape(4, 16)
                sbox_row = int(format(((ord(sbox_inputs[sbox_index][0]) -48 )%10)) + format(((ord(sbox_inputs[sbox_index][-1]) -48 )%10)),2) 
                sbox_col = int(format(((ord(sbox_inputs[sbox_index][1]) -48 )%10)) + format(((ord(sbox_inputs[sbox_index][2]) -48 )%10))+ format(((ord(sbox_inputs[sbox_index][3]) -48 )%10))+ format(((ord(sbox_inputs[sbox_index][4]) -48 )%10)),2) 
                sbox_output = format(sbox_matrix[sbox_row][sbox_col], "04b")
                sbox_outputs.append(sbox_output)
                
            #permutation P
            permuted_f_bits = []
            f_before_perm = "".join(sbox_outputs)
            for o in P:
                permuted_f_bits.append(f_before_perm[o-1])
            f_after_perm="".join(permuted_f_bits)
            
            f_int = int(f_after_perm, 2)
            next_right_half = format(operator.xor(f_int, int(L, 2)), '032b')
            
            next_left_half = R 
            
            new_left_halves.append(next_left_half)  
            new_right_halves.append(next_right_half)  
            L = next_left_half
            R = next_right_half
        
        IP1=[40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
        final_perm_bits=[]
        r16_l16_concat = str(new_right_halves[-1]) + str(new_left_halves[-1])
        for i in IP1:
            final_perm_bits.append(r16_l16_concat[i-1])
        ciphertext_binary = "".join(final_perm_bits)
        final.append((format(int(ciphertext_binary,2),"016X")))
    return("".join(final))
    
    
    
    
    
def CipherDecode(mode="decode",PlainText="", KeyText=""):
    raw_key_binary = convert_to_binary(KeyText)
    textsplit = []
    i=0
    while len(textsplit) < (len(raw_key_binary)//64):
        textsplit.append(raw_key_binary[i:i+64])
        i+=64
    
    pc1= [57,49,41,33,25,17,9,1,58,50,42,34,26,
          18,10,2,59,51,43,35,27,19,11,3,60,52,44,
          36,63,55,47,39,31,23,15,7,62,54,46,38,30,
          22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
    pc1_key_bits=[]
    
    #for j in range(len(textsplit)):
    for i in pc1:
        pc1_key_bits.append(textsplit[0][i-1])
    pc1_key_string = []
    
    k=0
    while len(pc1_key_string) <= (int(len(pc1_key_bits)/56)):
        pc1_key_string.append("".join(pc1_key_bits[k:k+56]))
        k+=56
    
    left_key_half = "".join(pc1_key_string[0][:28])
    right_key_half = "".join(pc1_key_string[0][28:])
    
      
    LeftShift = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]
    left_half_schedule  = [left_key_half]
    right_half_schedule  = [right_key_half]
    for shift_amount in LeftShift:
        current_left_half = left_half_schedule[-1]
        current_right_half = right_half_schedule[-1]
        shiftC = current_left_half[shift_amount:]  + current_left_half[:shift_amount]
        shiftD = current_right_half[shift_amount:] + current_right_half[:shift_amount]
        left_half_schedule.append(shiftC)
        right_half_schedule.append(shiftD)
    #second iteration
    combined_key_halves = list(zip(left_half_schedule,right_half_schedule))
    
    pc2 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
        
    subkey_bits= []
    for i1 in range(1,17):
        p = "".join(combined_key_halves[i1])
        for f in pc2:
            subkey_bits.append(p[f-1])
    all_subkeys_string = "".join(subkey_bits)
    subkey_index = 0
    subkeys = []
    while len(subkeys)!=16:
        subkeys.append(all_subkeys_string[subkey_index:subkey_index+48])
        subkey_index+=48
    
    subkeys = subkeys[::-1]
    
    plaintext_hex = convert_to_hex(PlainText)
    plaintext_nibbles = []
    for i in plaintext_hex:
        if i.isdigit():
           digit = format(((ord(i) -48 )%10),"04b")
           plaintext_nibbles.append(digit)
        elif i.isalpha():
           alpha = format(ord(i)-55,"04b")
           plaintext_nibbles.append(alpha)
    
    plaintext_binary1 = "".join(plaintext_nibbles)
    #print(len(plaintext_binary1))
    
    final = []
    for z in range(0,len(plaintext_binary1),64):
        plaintext_binary = plaintext_binary1[z:z+64]
        half_block_size = int((len(plaintext_binary)/2))
        left_plaintext = " ".join(plaintext_binary[:half_block_size])
        right_plaintext = " ".join(plaintext_binary[half_block_size:])
        
        IP = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,
              12,4,62,54,46,38,30,22,14,6,64,56,48,40,
              32,24,16,8,57,49,41,33,25,17,9,1,59,51,
              43,35,27,19,11,3,61,53,45,37,29,21,13,5,
              63,55,47,39,31,23,15,7]
        
        
        ip_bits=[]
        for i in IP:
            ip_bits.append(plaintext_binary[i-1])
        ip_half_size = int((len(ip_bits)/2))
        ip_left_half = "".join(ip_bits[:ip_half_size])
        ip_right_half = "".join(ip_bits[ip_half_size:])
        
        first_subkey  =subkeys[0]
        feistel_input = ip_right_half 
        
        E_BITSELECTIONTABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
        expanded_bits=[]
        for i in E_BITSELECTIONTABLE:
            expanded_bits.append(feistel_input[i-1])
        expanded_half = "".join(expanded_bits)
        
        expanded_int = int(expanded_half, 2)
        subkey_int = int(first_subkey, 2)
        xor_result = format(operator.xor(expanded_int, subkey_int), '048b')
        six_bit_groups = []
        group_index = 0 
        while len(six_bit_groups) != 8:
            six_bit_groups.append(xor_result[group_index:group_index+6])
            group_index+=6
        E_BITSELECTIONTABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
        P =[16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
        matrixS =[
        [
        14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
        0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
        4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
        15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13
        ],
            
                
        [
        15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
        3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
        0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
        13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9
        ],
        
        [
        10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
        13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
        13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
        1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12
        ],
        
        [
        7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
        13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
        10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
        3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14
        ],
        
        [
        2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
        14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
        4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
        11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3
        ],
            
        [
        12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
        10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
        9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
        4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13
        ],
        
        [
        4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
        13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
        1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
        6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12
        ],
            
        [
        13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
        1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
        7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
        2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11
        ]
        ]
        #second
        new_right_halves = []
        new_left_halves = []
        L = ip_left_half
        R = ip_right_half
        for round_number in range(16):
            expanded_bits=[]
            for v in E_BITSELECTIONTABLE:
                expanded_bits.append(R[v-1])
            expanded_half = "".join(expanded_bits)
            
            expanded_int = int(expanded_half, 2)
            subkey_int = int(subkeys[round_number], 2)
            xor_result = format(operator.xor(expanded_int, subkey_int), '048b')
            
            six_bit_groups = []
            group_index = 0 
            while len(six_bit_groups) != 8:
                six_bit_groups.append(xor_result[group_index:group_index+6])
                group_index+=6
                
            sbox_inputs  = six_bit_groups 
            sbox_outputs =[]
            for sbox_index in range(len(sbox_inputs)):
                sbox_matrix = np.array(matrixS[sbox_index][:]).reshape(4, 16)
                sbox_row = int(format(((ord(sbox_inputs[sbox_index][0]) -48 )%10)) + format(((ord(sbox_inputs[sbox_index][-1]) -48 )%10)),2) 
                sbox_col = int(format(((ord(sbox_inputs[sbox_index][1]) -48 )%10)) + format(((ord(sbox_inputs[sbox_index][2]) -48 )%10))+ format(((ord(sbox_inputs[sbox_index][3]) -48 )%10))+ format(((ord(sbox_inputs[sbox_index][4]) -48 )%10)),2) 
                sbox_output = format(sbox_matrix[sbox_row][sbox_col], "04b")
                sbox_outputs.append(sbox_output)
                
            #permutation P
            permuted_f_bits = []
            f_before_perm = "".join(sbox_outputs)
            for o in P:
                permuted_f_bits.append(f_before_perm[o-1])
            f_after_perm="".join(permuted_f_bits)
            
            f_int = int(f_after_perm, 2)
            next_right_half = format(operator.xor(f_int, int(L, 2)), '032b')
            
            next_left_half = R 
            
            new_left_halves.append(next_left_half)  
            new_right_halves.append(next_right_half)  
            L = next_left_half
            R = next_right_half
        
        IP1=[40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
        final_perm_bits=[]
        r16_l16_concat = str(new_right_halves[-1]) + str(new_left_halves[-1])
        for i in IP1:
            final_perm_bits.append(r16_l16_concat[i-1])
        ciphertext_binary = "".join(final_perm_bits)
        final.append((format(int(ciphertext_binary,2),"016X")))
    return("".join(final))





