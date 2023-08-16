"""
Generator gitarovych akordov
Maximilian Pandy, Praha, MFF UK, Obecna matematika, Bakalarske studium, 1. rocnik
Letny semester 2022/2023
Programovani 2
"""

import tkinter #knižnica na vykreslovanie

#tóny a poltóny na hmatníku gitary (susedné sú vzdialené o poltón)
chromatic=['C','C#','D','D#','E','F','F#','G','G#','A','A#','H']
#názvy tónov získaných zahratím prázdnych strún
strings=['E','A','D','G','H','E']

#súradnice potrebné k vykreslovaniu hmatov
x=[26]+[89+59.75*i for i in range(12)]
y=[253-29.5*i for i in range (6)]

mod=len(chromatic)

#####################Generovanie akordov#####################

#určenie z akých tónov sa akord skladá využitím hudobnej teórie
#dur: 3 tóny, 1. sa zhoduje s menom akordu, 2. je na vzdialenosť 4 poltónov a 3. na 7
#mol: obdobne, vzdialenosti sú 3 a 7 poltónov od 1.
def find_chord(root,scale):
    #root,scale: meno akordu v tvare tón/poltón zo zoznamu chromatic, dur/mol 

    root_pos=chromatic.index(root.capitalize())
    if scale=='mol':    
        return [chromatic[root_pos],chromatic[(root_pos+3)%mod],chromatic[(root_pos+7)%mod]]
    elif scale=='dur':
        return [chromatic[root_pos],chromatic[(root_pos+4)%mod],chromatic[(root_pos+7)%mod]]

#určenie všetkých pozícií kde sa daný tón na gitare vyskytuje    
def find_note(note,used_strings=[]):
    positions=[]
    for i in range (len(strings)):

        if i not in used_strings: 
            counter=0
            while counter!=13: #tón hľadáme po 12. pražec (pre pohodlnosť zahratia akordu)
                start=chromatic.index(strings[i])
                fret_note=chromatic[(start+counter)%mod]
                if fret_note==note:
                    positions.append((i,counter))
                    #pozíciu ukladáme ako dvojicu, (č. struny,č. pražca)
                counter+=1      
    return positions

candidate=[]
dist=[]
chords=[]

#nájdenie zahratelných trojíc tónov
def find_candidate(triad,index=0,used_strings=[]):
    #triad: hľadaná trojica tónov
    #index: počet už vybratých pozícií tónov
    #used_strings: ak už hráme tón na nejakej strune,
    #danú strunu nevieme použiť na zahratie ďalšieho tónu
    
    if index==3:
        #overenie či sa daná trojica dá chytiť na hmatníku,
        #tóny by nemali byť vzdialené viac ako 3 pražce od seba
        l=[i for i in dist if i!=0]
        if len(l)==0 or max(l)-min(l)<=3:
            chords.append(candidate.copy())
        return

    #rekurzívne hľadanie kandidátov na zahratelnú trojicu tónov   
    for solution in find_note(triad[index],used_strings):
        
        candidate.append(solution)
        
        dist.append(solution[1])        
        used_strings.append(solution[0])
        
        find_candidate(triad,index+1,used_strings)

        candidate.pop()
        dist.pop()
        used_strings.pop()
        
#####################Grafické rozhranie#####################

number=0 #poradové číslo hmatu

def vykreslit():
    
    global number,chords

    chord=e.get().split()
    #update plátna
    e.delete(0,'end')
    c.delete('nadpis','cislo')
    c.unbind('<Button-1>')
    number=0 

    #kontrola správnosti vstupu
    if len(chord)!=2 or chord[0] not in chromatic or (chord[1]!='mol' and chord[1]!='dur'):
        c.create_text(400,50,text='Neplatný vstup',fill='red', font='Arial 25 bold',tag='nadpis')
        return
    
    #nájdenie všetkých hmatov
    chords=[]
    triad=find_chord(chord[0],chord[1])
    find_candidate(triad)
    
    c.create_text(400,50,text=' '.join(chord),fill='blue', font='Arial 25 bold',tag='nadpis')
    c.create_line(440, 360, 500, 360, arrow=tkinter.LAST, width=14, fill='green',tag='nadpis')
    c.create_line(360, 360, 300, 360, arrow=tkinter.LAST, width=14, fill='green',tag='nadpis')
    c.create_text(400, 360,text=number+1,fill='blue', font='Arial 25 bold',tag='cislo')

    #vykreslenie hmatov využitím zoznamov súradnic zo začiatku
    for i in range (3):
        f=x[chords[number][i][1]]
        s=y[chords[number][i][0]]
        r=11.5
        c.create_oval(f-r,s+r,f+r,s-r,fill='orange',outline='',tag='cislo')
    #ľavým tlačidlom myše voláme funkciu refresh
    c.bind('<Button-1>',refresh)

width=18

#funkcia, ktorá vykreslí nový hmat v prípade, že ťukneme na jednu zo šipiek na plátne
def refresh(poz):
    #poz: nutný parameter, umožňuje nám zistiť napr. súradnice ťuknutia myše
    global number
    
    if 440<=poz.x<=500 and 360-width<=poz.y<=360+width:
        number=(number+1)%len(chords)

    elif 300<=poz.x<=360 and 360-width<=poz.y<=360+width:
        number=(number-1)%len(chords)
    
    c.delete('cislo')
    c.create_text(400, 360,text=number+1,fill='blue', font='Arial 25 bold',tag='cislo')

    for i in range (3):

        f=x[chords[number][i][1]]
        s=y[chords[number][i][0]]
        r=11.5
        c.create_oval(f-r,s+r,f+r,s-r,fill='orange',outline='',tag='cislo')

#vytvorenie okna, entry boxu, tlačidla a plátna       
okno=tkinter.Tk()
okno.title('Akordy')
okno.geometry('800x500')

tkinter.Label(text='Zadajte akord').pack()
e=tkinter.Entry()
e.pack()
#stlačením tlačidla voláme funkciu vykresliť
b=tkinter.Button(text='Generovať',width=15,command=vykreslit)
b.pack()

c=tkinter.Canvas(w=800,he=450,bg='white')
c.pack()

#umiestnenie obrazu na plátno
fretboard=tkinter.PhotoImage(file='fretboard.png')
obraz=c.create_image(10,200,image=fretboard,anchor='w')

okno.mainloop()
