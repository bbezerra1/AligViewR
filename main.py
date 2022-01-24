import threading
from tkinter import *


# Read FASTA files
def fastaread(arq):
    data = []
    # seq = ''
    sequence = []
    y = open(arq, 'r')

    line = y.readline().rstrip()
    if not line.startswith('>'):
        raise Exception('Records in FASTA files should start with ">" character')

    while line:
        try:
            if line[0] == '>':
                data.append(sequence)
                sequence = Sequence(line[1:].rstrip())  # cria o objeto
                line = y.readline()

            elif not line.rstrip():
                line = y.readline()

            else:
                [sequence.append(i) for i in list(line)]  # para adicionar residuo por residuo
                line = y.readline()

        except EOFError:
            data.append(sequence)
            y.close()
            break

    data.pop(0)
    return data


# Classe das sequencias
class Sequence:
    def __init__(self, name):
        self._name = name
        self._residues = []

    def __getitem__(self, item):
        return self._residues[item]

    def append(self, value):
        self._residues.append(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def __str__(self):
        return f'{self.name} - {" ".join(self._residues)}'


# Classe da tela
class App:
    def __init__(self, sequences):
        # Inicia a tela
        self.root = Tk()
        self.tela()

        # Frames
        self.alig_frame = Frame(self.root, width=1025, height=720)
        self.seq_frame = Frame(self.root, width=250, height=720)

        # Scrollbar set
        self.v_scrollbar = Scrollbar(self.root)
        self.v_scrollbar.pack(side='right', fill=Y)
        self.h_scrollbar = Scrollbar(self.root, orient=HORIZONTAL)
        self.h_scrollbar.pack(side='bottom', fill=X)

        # Canvas
        self.alig_canvas = Canvas(self.alig_frame, bg='#E5E5E5', width=1025, height=720, yscrollcommand=self.v_scrollbar
                                  .set, xscrollcommand=self.h_scrollbar.set)
        self.seq_canvas = Canvas(self.seq_frame, width=250, height=720,  yscrollcommand=self.v_scrollbar.set)

        # Variaveis posicionais
        self.y = 20
        self.x = 5

        # Chama as funcoes
        self.items_place()
        self.frames_tela(sequences)
        self.scroll_config()

        # Mainloop
        self.root.mainloop()

    # Funcao simples de confs basicas da tela
    def tela(self):
        self.root.title("AligViewR")
        self.root.configure(background='#1e3743')
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

    def multiple_yview(self, *args):
        self.alig_canvas.yview(*args)
        self.seq_canvas.yview(*args)

    def items_place(self):
        # Pack dos frames
        self.alig_frame.place(x=255, y=0)
        self.seq_frame.place(x=0, y=0)
        # Place dos canvas
        self.alig_canvas.place(x=0, y=0)
        self.seq_canvas.place(x=0, y=0)

    # Scrollbar config
    def scroll_config(self):
        # Set the right vars to scroll region
        i, j, xs, ys, = self.alig_canvas.bbox('all')

        self.alig_canvas.configure(scrollregion=(i+10, j, xs+10, ys,))  # Max de scroll de acordo com as seqs
        self.v_scrollbar.config(command=self.multiple_yview)
        self.h_scrollbar.config(command=self.alig_canvas.xview)

    def frames_tela(self, sequences):
        for sequence in sequences:
            # Cria o texto da sequencia no canvas
            self.seq_canvas.create_text(100, self.y, text=sequence.name, justify='left')

            for nucleotide in sequence:
                if nucleotide == 'A':
                    a = self.alig_canvas.create_text(self.x, self.y, text=nucleotide)
                    r = self.alig_canvas.create_rectangle(self.x-6, self.y-7, self.x+6, self.y+8, fill='#ef476f',
                                                          outline='')

                elif nucleotide == 'G':
                    a = self.alig_canvas.create_text(self.x, self.y, text=nucleotide)
                    r = self.alig_canvas.create_rectangle(self.x-6, self.y-7, self.x+6, self.y+8, fill='#ffd166',
                                                          outline='')

                elif nucleotide == 'T':
                    a = self.alig_canvas.create_text(self.x, self.y, text=nucleotide)
                    r = self.alig_canvas.create_rectangle(self.x-6, self.y-7, self.x+6, self.y+8, fill='#06d6a0',
                                                          outline='')

                elif nucleotide == 'C':
                    a = self.alig_canvas.create_text(self.x, self.y, text=nucleotide)
                    r = self.alig_canvas.create_rectangle(self.x-6, self.y-7, self.x+6, self.y+8, fill='#118ab2',
                                                          outline='')

                else:
                    a = self.alig_canvas.create_text(self.x, self.y, text=nucleotide)
                    r = self.alig_canvas.create_rectangle(self.x-6, self.y-7, self.x+6, self.y+8, fill='#E5E5E5',
                                                          outline='')

                self.alig_canvas.tag_lower(r, a)
                self.alig_canvas.pack()
                self.x += 20

            self.y += 18
            self.x = 5


def main():
    # a = fastaread('ds_maldehy_431s_gins_90gt.fasta')
    # a = fastaread('tplg_ds_isodehy_ginsi_gt75.fasta')
    a = fastaread(input('File name:\n'))

    App(a)


if __name__ == '__main__':
    main()
