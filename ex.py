import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Tkinter 창 설정
root = tk.Tk()

# Matplotlib Figure 객체 생성 및 그래프 추가
fig = Figure(figsize=(5, 4), dpi=100)
plot = fig.add_subplot(111)
plot.plot([0, 1, 2], [0, 1, 4])

# 그래프 제목 추가
plot.set_title("그래프 이름")

# Canvas에 Figure 추가
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Tkinter 이벤트 루프 시작
root.mainloop()