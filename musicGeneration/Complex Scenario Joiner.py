import math
import wave
import struct
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
from alive_progress import alive_bar
from time import sleep
from progress.bar import IncrementalBar


class Beat:
    def __init__(self, index, volume):
        self.index = index
        self.volume = volume


def GetTiles(frames, rate, pick, maxTPS, saveName):
    workframes = [abs(item) for item in frames]

    silentLimit = max(workframes) * 0.2

    # x = np.arange(0, len(workframes), 1)
    # plt.plot(x, workframes)
    # plt.plot(0, silentLimit, 'r.', 'MarkerSize', 50)
    # plt.show()

    # print (len(workframes) / rate / 2)
    pies = []

    print(">>> Генерация паев... ", end='')
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
    with alive_bar(len(pies), title='Анализ паев', bar='smooth') as bar:
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

            # print(f"Adding {iter} times for {rate}")
            for i in beatpointsIndexCompleted:
                i.index += iter * rate

            # print ([item.index for item in beatpointsIndexCompleted])

            # print([item.index for item in complexPie])
            totalBeats.extend(beatpointsIndexCompleted)
            # print(f"Analyzing... {round(pieInd / len(pies) * 100, 2)}% ({pieInd} / {len(pies)})")
            iter += 1
            bar()

    totalBeats.sort(key=lambda x: x.index)

    print(">>> Тайлы получены")
    print(">>> Создание комплексного пая")
    complexTiles = []
    addedIndex = 0
    t = 0
    # with alive_bar(len(frames), title='Генерация комплексного пая', bar='smooth') as bar:
    # for i in range(0, len(frames)):
    #     if len(totalBeats) > 0:
    #         empty = True
    #         for b in totalBeats:
    #             if b.index == i:
    #                 empty = False
    #         if empty:
    #             complexTiles.append(Beat(0, 0))
    #         else:
    #             complexTiles.append(totalBeats[addedIndex])
    #             addedIndex += 1
    #     else:
    #         complexTiles.append(Beat(0, 0))
    #     bar()
    complexTiles = []
    print(len(totalBeats))
    with alive_bar(len(totalBeats), title='Генерация комплексного пая', bar='smooth') as bar:
        for bIndex, bValue in enumerate(totalBeats):
            if bIndex == 0:
                print(bValue.index)
                complexTiles.extend([Beat(0, 0)] * (bValue.index - 1))
                complexTiles.append(bValue)
            else:
                complexTiles.extend([Beat(0, 0)] * (bValue.index - totalBeats[bIndex - 1].index - 1))
                complexTiles.append(bValue)
                if bIndex == len(totalBeats) - 1:
                    print(bValue.index)
                    print(len(frames) / 2 - bValue.index + 1)
                    complexTiles.extend([Beat(0, 0)] * int((len(frames) / 2 - bValue.index)))
            bar()
    # x = np.arange(0, len(workframes), 1)
    # plt.plot(x, workframes)
    # plt.plot(0, silentLimit, 'r.', 'MarkerSize', 50)

    tb = []
    for i in complexTiles:
        tb.append(i)

    # plt.show()

    print(f'Done with {len(tb)}')
    return tb


def isNoneBeats(pie):
    return pie.count(0) == len(pie)


# MUSIC FILE TAG
sourceMusic = wave.open(
    "C:\\Users\\Администратор\\Downloads\\WhatElse [music].wav",
    mode='rb')

framesCount = sourceMusic.getnframes()
rate = sourceMusic.getframerate()

print(f"Количество фреймов: {framesCount}\nФреймрейт: {rate}\nДлина аудиофайла (сек.): {framesCount / rate}")

print("Чтение фреймов...")
frames = sourceMusic.readframes(framesCount)
print("Фреймы считаны. Анализируем...")

frames = struct.unpack("<" + str(framesCount * 2) + "h", frames)

framesList = list(frames)
print(len(framesList))

maxFrame = max(framesList)
minFrame = min(framesList)

print(f"Макс: {maxFrame}\nМин: {minFrame}\nАмплитуда: ~{(maxFrame - minFrame) / 2}")

print("-------------НАСТРОЙКА-------------")
print("-------------ШАБЛОНЫ ПИКОВ-------------")

print(">>> Getting Tiles Music")
MusicTiles = GetTiles(framesList, rate, 0.7, 2, "DushnoDuetMusic")
with alive_bar(len(MusicTiles), title='Корректировка тайлов', bar='smooth') as bar:
    for i in MusicTiles:
        i.index /= 2
        bar()

# f = open ("C:\\Users\\Администратор\\Documents\\CANTO\\testmusic.til", "w")
# p = [item.index for item in MusicTiles if item.volume > 0]
# for i in p:
#     f.write(f"{i / rate}\n")
#
# f.close()

# plt.plot (np.arange(0, len(MusicTiles)), [i.volume for i in MusicTiles])
# plt.show()

print([item.index for item in MusicTiles if item.index != 0][:20])

# VOCAL FILE TAG
sourceVocals = wave.open(
    "C:\\Users\\Администратор\\Downloads\\WhatElse [vocals].wav",
    mode='rb')

framesCount = sourceVocals.getnframes()
rate = sourceVocals.getframerate()

print(f"Количество фреймов: {framesCount}\nФреймрейт: {rate}\nДлина аудиофайла (сек.): {framesCount / rate}")

print("Чтение фреймов...")
frames = sourceVocals.readframes(framesCount)
print("Фреймы считаны. Анализируем...")

frames = struct.unpack("<" + str(framesCount * 2) + "h", frames)
framesList = list(frames)

print(">>> Getting Tiles Vocals")
VocalTiles = GetTiles(framesList, rate, 0.9, 5, "DushnoDuetVocals")
with alive_bar(len(VocalTiles), title='Корректировка тайлов', bar='smooth') as bar:
    for i in VocalTiles:
        i.index /= 2
        bar()

# plt.plot (np.arange(0, len(VocalTiles)), [i.volume for i in VocalTiles])
# plt.show()

# f = open ("C:\\Users\\Администратор\\Documents\\CANTO\\testvocal.til", "w")
# p = [item.index for item in VocalTiles if item.volume > 0]
# for i in p:
#     f.write(f"{i / rate}\n")
#
# f.close()

print([item.index for item in VocalTiles if item.index != 0][:20])
# print (f"Пик 1500; TPS 3 = {GetTileCountByPicks(frames, rate, 1500, 3)} нот")
# print (f"Пик 2500; TPS 3 = {GetTileCountByPicks(frames, rate, 2500, 3)} нот")
# print (f"Пик 3500; TPS 3= {GetTileCountByPicks(frames, rate, 3500, 3)} нот")
# print (f"Пик 4500; TPS 3 = {GetTileCountByPicks(frames, rate, 4500, 3)} нот")

finalBeats = []
with alive_bar(math.ceil(len(frames) / rate / 2), title='Генерация комплексного пая всего произведения',
               bar='smooth') as bar:
    for i in range(math.ceil(len(frames) / rate / 2)):
        print(f"Обрабатываю {i}-й пай ", end='Результат: ')
        if (i + 1) * rate > len(frames) / 2:
            musicPie = MusicTiles[i * rate:int(len(frames) / 2)]
            vocalPie = VocalTiles[i * rate:int(len(frames) / 2)]
        else:
            musicPie = MusicTiles[i * rate:(i + 1) * rate]
            vocalPie = VocalTiles[i * rate:(i + 1) * rate]
        if isNoneBeats([int(item.index) for item in vocalPie]):
            finalBeats.extend(musicPie)
            print("Музыка")
        else:
            finalBeats.extend(vocalPie)
            print("Вокал")
        bar()

print(f"Done with {len(finalBeats)}")
print(">>> Генерация плота...")
print(f"Битов: {len([item for item in finalBeats if item.index != 0])}")
print([item.index for item in finalBeats if item.index != 0][:20])
plt.plot(np.arange(0, len(frames) / 2), [item.volume for item in finalBeats])
plt.show()
print([x.index / rate for x in finalBeats if x.index != 0][:10])

# WRITING TILES
tiles = open('D:\\CantoNew\\test.til', 'w')
for x in [x.index / rate for x in finalBeats if x.index != 0]:
    tiles.write(str(x) + "\n")

tiles.close()
print('Done')