from typing import Dict
import os

C = {  #C
    'k':'क', 
    'kh':'ख',
    'K':'ख', 
    'g':'ग',
    'gh':'घ',
    'G':'घ', 
    'c':'च',
    'ch':'छ', 
    'C':'छ', 
    'j':'ज',
    'jh':'झ',
    'J':'झ', 
    'J':'ञ',
    'T':'ट', 
    't':'त',
    'Th':'ठ',
    'th':'थ',
    'D':'ड',
    'd':'द',
    'Dh':'ढ',
    'dh':'ध',
    'N':'ण', 
    'n':'न',
    'p':'प',
    'ph':'फ',
    'P':'फ',
    'F':'फ',
    'b':'ब',
    'bh':'भ',
    'B':'भ', 
    'm':'म',
    'y':'य',
    'r':'र',
    'l':'ल',
    'v':'व',
    'z':'श',
    'sh':'श', 
    'S':'ष',
    's':'स',
    'h':'ह',
    'L':'ळ',
    'kS':'क्ष',
    'kSh':'क्ष',
    'ksh':'क्ष',
    'x':'क्ष', 
    'jJ':'ज्ञ',
    'dny':'ज्ञ',
    'gny':'ज्ञ', 
    'zr':'श्र',
    'shr':'श्र', 
    'q':'क़',
    'X':'ख़',
    'Y':'ग़',
    'z':'ज़',
    'f':'फ़',
    'G':'ड़',
    '':'य़',
    '':'ऩ', # for transcribing Dravidian alveolar n ≡ 0928 न  093C $
    '':'ऱ', #for transcribing Dravidian alveolar r. Half form is eyelash RA ≡ 0930 र  093C $
    '':'ऴ', #for transcribing Dravidian l ≡ 0933 ळ  093C $़
    'Rh':'ढ़',
    'IR':'ऌ',
    'IL':'ॡ',
    '':'ऎ', #Kashmiri, Bihari languages. Dravidian short e
    '':'\u097B', #SINDHI IMPLOSIVE ॻ
    '':'\u097C', #SINDHI IMPLOSIVE ॼ
    '':'\u097E', #SINDHI IMPLOSIVE ॾ
    '':'\u097F', #SINDHI IMPLOSIVE ॿ
    '':'\u0978', # ॸ DEVANAGARI LETTER MARARI DDA 
    '':'\u0979', # ॹ DEVANAGARI LETTER ZHA. used in transliteration of Avestan
    '':'\u097A', # ॺ DEVANAGARI LETTER HEAVY YA. used for an affricated glide JJYA
    '':'\u097D', # ॽ DEVANAGARI LETTER GLOTTAL STOP
}



v = {  #MATRAS
    'aa':'ा', 
    'a':'ा', 
    'A':'ाा', 
    'i':'ि',
    'ii':'ी', 
    'I':'ी',
    'ee':'ी', 
    'u':'ु',
    'uu':'ू',
    'U':'ू',
    'oo':'ू', 
    'UU':'ृ', #######"kru"
    'e':'े',
    'ai':'ै',
    'E':'ै',
    'o':'ो',
    'au':'ा'+'ै',
    'ou':'ा'+'ै',
    'EE':'ॅ',
    'aE':'ॅ',
    '':'ॉ',      #DEVANAGARI VOWEL SIGN CANDRA O
    '':'\u094F', #Kashmiri and Bihari $ॏ
    '':'\u094A', #Kashmiri and Bihari, also short e $ॊ
    '':'\u093A', #Kashmiri and Bihari ऺ  
    '':'\u093B', #Kashmiri and Bihari $ऻ 
    '':'\u0944', # ॄ
    '':'\u094E', # ॎ DEVANAGARI VOWEL SIGN PRISHTHAMATRA E . Historic Use only
    '':'\u0955', # ॕ AVESTAN. DEVANAGARI VOWEL SIGN CANDRA LONG E. 
    '':'\u0956', #KASHMIRI . DEVANAGARI VOWEL SIGN UE
    '':'\u0957', #KASHMIRI . DEVANAGARI VOWEL SIGN UUE
    'L':'\u0962', # SANSKRIT ॢ
    'LL':'\u0963', # SANSKRIT ॣ
}

V = { #VOWELS
    'a':'अ',
    'aa':'आ',
    'A':'आ',   
    'i':'इ',
    'ii':'ई',
    'I':'ई',
    'ee':'ई',
    'u':'उ',
    'uu':'ऊ',
    'U':'ऊ',
    'oo':'ऊ',
    'e':'ए',
    'ai':'ऐ',
    'E':'ऐ',
    'EE':'ऍ', 
    'aE':'ऍ', 
    'o':'ओ',
    'au':'औ',
    'ou':'औ',
    'oN':'ऑ', 
    'R':'ऋ',  
    'RR':'ॠ', #SANSKRIT
    'LL':'ॡ', #SANSKRIT
    '':'ॲ',# Marathi
    '':'ऄ', #used for short e in Awadhi. also transliterated kashmiri and south indian languages
    '':'ॵ', #Kashmiri and Bihari
    '':'\u0973', #Kashmiri and Bihari ॳ
    '':'\u0974', #Kashmiri and Bihari ॴ
    '':'\u0976', #Kashmiri  ॶ
    '':'\u0977', #Kashmiri  ॷ
}

misc = { # VOWEL MODIFIERS(m), HALANT(H), NUKTA(N), NUMBERS, CURRENCY
    'M':'ं',
    'H':'ः',
    'MM':'ँ',
    '.a':'ऽ',
    'w':'्',
    'NN':'◌़', ##dashboard for special chars? how to type ण?
    ' ':' ',
    '.':'।',
    '>':'॥',
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
    '-':'\u200D', #zero width joiner
    '_':'\u200C', #zero widhth non joiner
    '':'\u0900', #DEVANAGARI SIGN INVERTED CANDRABINDU 
    '':'\u0951', #VEDIC TONE MARK. DEVANAGARI STRESS SIGN UDATTA. 
    '':'\u0952', #VEDIC TONE MARK. DEVANAGARI STRESS SIGN ANUDATTA ॒
}

def generate_mapping_table(title: str, data: Dict[str, str]) -> str:
    table = f"| Roman | Devanagari |\n| --- | --- |\n"
    for roman, devanagari in data.items():
        table += f"| {roman} | {devanagari} |\n"
    return f"## {title}\n{table}"

def generate_guidebook() -> str:
    guidebook = "# Devanagari Character Mapping Guidebook\n\n"
    guidebook += "This guidebook explains the mapping between Roman and Devanagari characters used in the custom text editor. When you type the Roman characters, the corresponding Devanagari characters will be displayed.\n\n"
    guidebook += generate_mapping_table("Consonants", C)
    guidebook += "\n\n"
    guidebook += generate_mapping_table("Vowels", V)
    guidebook += "\n\n"
    guidebook += generate_mapping_table("Vowels", v)
    guidebook += "\n\n"
    guidebook += generate_mapping_table("Vowel Modifiers, Halant, Nukta, and Other Symbols", misc)
    guidebook += "\n\nRemember, the mapping is case-sensitive. Enjoy using the custom text editor!"
    return guidebook

if __name__ == "__main__":
    guidebook = generate_guidebook()
    with open("devanagari_mapping_guidebook.md", "w", encoding="utf-8") as f:
        f.write(guidebook)
    print("Guidebook generated successfully!")