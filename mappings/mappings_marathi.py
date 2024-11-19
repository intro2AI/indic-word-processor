C = {  #C
    'k':'क', 
    'kqh':'ख',
    'g':'ग',
    'gqh':'घ',
    'ch':'च',
    'chqh':'छ', 
    'j':'ज',
    'jqh':'झ',
    'T':'ट', 
    't':'त',
    'Tqh':'ठ',
    'tqh':'थ',
    'D':'ड',
    'd':'द',
    'Dqh':'ढ',
    'dqh':'ध',
    'N':'ण', 
    'n':'न',
    'p':'प',
    'pqh':'फ',
    'b':'ब',
    'bqh':'भ',
    'm':'म',
    'y':'य',
    'Y':'ञ',
    'r':'र',
    'l':'ल',
    'v':'व',
    'V':'ङ',
    'sqh':'श', 
    'S':'ष',
    's':'स',
    'h':'ह',
    'L':'ळ',
    'kqS':'क्ष',
    'kqSqh':'क्ष',
    'kqsqh':'क्ष',
    'dqnqy':'ज्ञ',
    'gqnqy':'ज्ञ', 
    'sqhqr':'श्र', 
    'Qk':'क़',
    'Qkqh':'ख़',
    'Qg':'ग़',
    'Qj':'ज़',
    'QP':'फ़',
    'QD':'ड़',
    'Qy':'य़',
    'Qn':'ऩ', # for transcribing Dravidian alveolar n ≡ 0928 न  093C $
    'Qr':'ऱ', #for transcribing Dravidian alveolar r. Half form is eyelash RA ≡ 0930 र  093C $
    'QL':'ऴ', #for transcribing Dravidian l ≡ 0933 ळ  093C $़
    'QDqh':'ढ़',
    'Qv':'व़',
    'Zg':'\u097B', #SINDHI IMPLOSIVE ॻ gZ
    'Zj':'\u097C', #SINDHI IMPLOSIVE ॼ jZ
    'ZD':'\u097E', #SINDHI IMPLOSIVE ॾ DZ
    'Zb':'\u097F', #SINDHI IMPLOSIVE ॿ bZ
    'DqDqA':'\u0978', # ॸ DEVANAGARI LETTER MARWARI DDA DDZ 
    'ZHA':'\u0979', # ॹ DEVANAGARI LETTER ZHA. used in transliteration of Avestan
    'JYqA':'\u097A', # ॺ DEVANAGARI LETTER HEAVY YA. used for an affricated glide # original in unicode: JJYA
    'ZK':'\u097D', # ॽ DEVANAGARI LETTER GLOTTAL STOP KZ 
}



v = {  #MATRAS
    'aa':'ा', 
    'a':'ा', 
    'i':'ि',
    'ii':'ी', 
    'ee':'ी', 
    'u':'ु',
    'uu':'ू',
    'oo':'ू', 
    'e':'े',
    'ai':'ै',
    'o':'ो',
    'au':'ा'+'ै',
    'ou':'ा'+'ै',
    #############
    'aE':'ॅ',
    'aO':'ॉ',
    'AO':'',
    'AE':'',      #DEVANAGARI VOWEL SIGN CANDRA O
    #######
    'zau':'\u094F', #Kashmiri and Bihari $ॏ right alt + ou
    'zo':'\u094A', #Kashmiri and Bihari, also short e $ॊ  right alt + o
    'ze':'ॆ',
    #######
    '':'\u093A', #Kashmiri and Bihari ऺ right alt
    '':'\u093B', #Kashmiri and Bihari $ऻ  
    '':'\u094E', # ॎ DEVANAGARI VOWEL SIGN PRISHTHAMATRA E . Historic Use only #right alt + a
    '':'\u0955', # ॕ AVESTAN. DEVANAGARI VOWEL SIGN CANDRA LONG E. #right alt+E
    '':'\u0956', #KASHMIRI . DEVANAGARI VOWEL SIGN UE #right alt +
    '':'\u0957', #KASHMIRI . DEVANAGARI VOWEL SIGN UUE #right alt +
    'Rru':'ृ', # #Rru
    'RrU':'\u0944', # ॄ #RrU
    'Lqlqi':'\u0962', # SANSKRIT ॢ
    'LqlqI':'\u0963', # SANSKRIT ॣ
}

V = { #VOWELS
    'a':'अ',
    'aa':'आ',
    'A':'अ',  #A
    'AA':'आ', #AA
    'i':'इ',
    'ii':'ई',
    'I':'इ', #A 
    'II':'ई', #AA
    'ee':'ई',
    'u':'उ',
    'uu':'ऊ',
    'U':'उ', #A 
    'UU':'ऊ', #AA
    'oo':'ऊ',
    'e':'ए',
    'ai':'ऐ',
    'E':'ए', #A 
    'EE':'ऐ', #AA
    #'aE':'ऍ', 
    'o':'ओ',
    'O':'ओ',
    'au':'औ',
    'AU':'औ',
    'ou':'औ',
    'RRu':'ऋ',  
    'RRU':'ॠ', #SANSKRIT
    'LqLqi':'ऌ',
    'LqLqI':'ॡ',
    ########    
    'zAU':'ॵ',       
    'zO':'\u0912',
    'zEE':'ऎ', 
    'zA':'ऄ',
    'zau':u"\u094F", #Kashmiri and Bihari $ॏ right alt + ou
    'zo':'\u094A', #Kashmiri and Bihari, also short e $ॊ  right alt + o
    'ze':'\u0943', #:'ॆ', 
    ##################
    '':'\u0973', #Kashmiri and Bihari ॳ
    '':'\u0974', #Kashmiri and Bihari ॴ
    '':'\u0976', #Kashmiri  ॶ #right alt +
    '':'\u0977', #Kashmiri  ॷ #right alt +````````````
    ##################
    'AO':'ऑ',
    'AE':'ॲ',# Marathi
    'aE':'',
    'aO':'',
    ################## 
} # ō  āō  Ē

misc = { # VOWEL MODIFIERS(m), HALANT(H), NUKTA(N), NUMBERS, CURRENCY
    'M':'ं',
    'H':'ः',
    'MM':'ँ',
    'F':'ऽ',
    'q':'्',
    '.N':'◌़', 
    ' ':' ',
    '.':'.',
    'f':'.',
    'ff':'॥',
    '':'\u0970', #DEVANAGARI ABBREVIATION SIGN
    '':'\u0971', #DEVANAGARI SIGN HIGH SPACING DOT
    '0':'०',
    '1':'१',
    '2':'२',
    '3':'३',
    '4':'४',
    '5':'५',
    '6':'६',
    '7':'७',
    '8':'८',
    '9':'९',
    'om':'ॐ',
    'OM':'ॐ',
    'AUM':'ॐ',
    'W':'\u200D', #zero width joiner
    'w':'\u200C', #zero widhth non joiner
    '':'\u0900', #DEVANAGARI SIGN INVERTED CANDRABINDU 
    '':'\u0951', #VEDIC TONE MARK. DEVANAGARI STRESS SIGN UDATTA. 
    '':'\u0952', #VEDIC TONE MARK. DEVANAGARI STRESS SIGN ANUDATTA ॒
}
#available keys and combinations
#ZXF
#.+''