import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
from alive_progress import alive_bar
from time import sleep


class Beat:
    def __init__(self, index, volume):
        self.index = index
        self.volume = volume


def GetTileCountByPicks(frames, rate, pick, maxTPS, saveName):
    workframes = [item for item in frames if item >= 0]

    silentLimit = max(workframes) * 0.6

    x = np.arange(0, len(workframes), 1)
    plt.plot(x, workframes)
    plt.plot(0, silentLimit, 'r.', 'MarkerSize', 50)
    plt.show()

    # print (len(workframes) / rate / 2)
    pies = []

    print(">>> Pies generation... ", end='')
    currentPieLimit = rate
    while len(pies) < math.ceil(len(workframes) / rate / 2):
        if currentPieLimit <= len(workframes):
            pies.append(workframes[currentPieLimit - rate:currentPieLimit])
        else:
            pies.append(workframes[currentPieLimit - rate:len(workframes)])
        currentPieLimit += rate
    sleep(2)
    print("DONE")

    totalBeats = []
    iter = 0
    for pieInd, pie in enumerate(pies):
        # print (f"Total: {len(pie)} | Unique: {len(set(pie))}")
        maxBeat = max(pie)
        maxBeatIndex = pie.index(maxBeat)
        minBeatLimit = maxBeat * pick
        tempPie = [item for item in pie if item > minBeatLimit]
        minBeat = min(tempPie)
        minBeatIndex = pie.index(minBeat)

        x = np.arange(0, len(pie), 1)
        y = pie

        beatpointsIndex = []
        for index, beat in enumerate(pie):
            if beat > minBeatLimit and beat > silentLimit:
                beatpointsIndex.append(Beat(index, beat))

        # print (f"Min: {minBeatLimit}")

        beatpointsIndex.sort(key=lambda x: x.volume)
        beatpointsIndex.reverse()

        x = np.arange(0, len(beatpointsIndex), 1)

        # plt.plot(x, [item.volume for item in beatpointsIndex])
        # plt.show()

        beatpointsIndexSorted = beatpointsIndex
        # print (beatpointsIndexSorted[:30])
        beatpointsIndexCompleted = []
        if len(beatpointsIndex) > 0:
            beatpointsIndexCompleted.append(beatpointsIndex[0])
        # plt.plot(beatpointsIndexCompleted[0].index, beatpointsIndexCompleted[0].volume, 'r.', 'MarkerSize', 50)
        i = 0
        for beat in beatpointsIndex:
            # if abs(beatpointsIndexCompleted[i].index - beat.index) >= rate / maxTPS:
            #     beatpointsIndexCompleted.append(beat)
            #     #plt.plot(beat.index, beat.volume, 'r.','MarkerSize', 50)
            #     i += 1
            #
            good = True
            for c in beatpointsIndexCompleted:
                if abs(c.index - beat.index) < rate / maxTPS:
                    good = False
            if good:
                # plt.plot(beat.index, beat.volume, "r.")
                beatpointsIndexCompleted.append(beat)

        # plt.plot(x, [item.volume for item in beatpointsIndex])
        # plt.show()

        # print (f"Completed beats len: {len(beatpointsIndexCompleted)} ({len(beatpointsIndexCompleted) / len(beatpointsIndexSorted) * 100}%)")

        # plt.plot(x, y, 'g')
        # plt.plot(maxBeatIndex, maxBeat, 'r.','MarkerSize', 5)
        # plt.plot(minBeatIndex, minBeat, 'r.', 'MarkerSize', 5)
        # plt.show()

        print(f"Adding {iter} times for {rate}")
        for i in beatpointsIndexCompleted:
            i.index += iter * rate

        print([item.index for item in beatpointsIndexCompleted])
        totalBeats.extend(beatpointsIndexCompleted)
        print(f"Analyzing... {round(pieInd / len(pies) * 100, 2)}% ({pieInd} / {len(pies)})")
        iter += 1

    totalBeats.sort(key=lambda x: x.index)

    til = open(f"C:\\Users\\Администратор\\Documents\\CANTO\\{saveName}.til", "w")

    for i in totalBeats:
        til.write(f"{i.index / rate}\n")

    x = np.arange(0, len(workframes), 1)
    plt.plot(x, workframes)
    plt.plot(0, silentLimit, 'r.', 'MarkerSize', 50)

    for i in totalBeats:
        plt.plot(i.index, i.volume, 'r.', 'MarkerSize', 50)

    # plt.show()

    print(f'Done with {len(totalBeats)}')


source = wave.open(
    "C:\\Users\\Администратор\\Downloads\\Payday_-_Big_Boy-_1_.wav",
    mode='rb')

framesCount = source.getnframes()
rate = source.getframerate()

print(f"Количество фреймов: {framesCount}\nФреймрейт: {rate}\nДлина аудиофайла (сек.): {framesCount / rate}")

print("Чтение фреймов...")
frames = source.readframes(framesCount)
print("Фреймы считаны. Анализируем...")

frames = struct.unpack("<" + str(framesCount * 2) + "h", frames)

framesList = list(frames)
print(len(framesList))

maxFrame = max(framesList)
minFrame = min(framesList)

print(f"Макс: {maxFrame}\nМин: {minFrame}\nАмплитуда: ~{(maxFrame - minFrame) / 2}")

print("-------------НАСТРОЙКА-------------")
print("-------------ШАБЛОНЫ ПИКОВ-------------")

GetTileCountByPicks(framesList, rate, 0.7, 5, "bigboutest")
# print (f"Пик 1500; TPS 3 = {GetTileCountByPicks(frames, rate, 1500, 3)} нот")
# print (f"Пик 2500; TPS 3 = {GetTileCountByPicks(frames, rate, 2500, 3)} нот")
# print (f"Пик 3500; TPS 3= {GetTileCountByPicks(frames, rate, 3500, 3)} нот")
# print (f"Пик 4500; TPS 3 = {GetTileCountByPicks(frames, rate, 4500, 3)} нот")
