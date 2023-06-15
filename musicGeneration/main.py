import math
import threading
import wave
import struct
import time

from alive_progress import alive_bar


def GetTileCountByPicks(frames, rate, pick, maxTPS, threadName):
    frames = [abs(item) for item in frames]
    maxPick = max(frames)
    maxSecPick = max(frames[:rate])

    pie = int(len(frames) / 10) * 3
    # pickLine = np.full(pie, maxPick - pick)
    # mp.title(f"rate: {rate}, pick: {pick}, maxTPS: {maxTPS} --- GENERAL")
    # mp.plot(range(0, pie), frames[:pie], 'b-', range(0, pie), pickLine, 'r--')
    # mp.show()

    print(f"[Вычисляем ноты с заданными параметрами rate: {rate}, pick: {pick}, maxTPS: {maxTPS}]")

    SuitableTilesInds = []
    SuitableTiles = []

    ind = 0
    sec = 0
    tmpTile = []
    # with alive_bar(len(frames), title=f'Обработка [{threadName}]', bar='smooth') as bar:
    for indexM, i in enumerate(frames):
        if i > maxPick - pick:
            tmpTile.append(i)
        else:
            tmpTile.append(maxPick + 1)

        if (ind % rate == 0):
            # sec += 1
            # startFrame = sec * rate
            # endFrame = (sec+1) * rate;
            # maxSecPick = max(frames[startFrame:endFrame])
            # print (f"Max pick: {maxSecPick}")
            # print(f"Проанализировано {round(indexM / len(frames) * 100, 2)}% ({indexM} / {len(frames)} фреймов)")
            while (len([item for item in tmpTile if item != maxPick + 1]) > maxTPS / 2):
                indToDelete = tmpTile.index(min(tmpTile))
                tmpTile[indToDelete] = maxPick + 1

            for index, item in enumerate(tmpTile):
                if (item == maxPick + 1):
                    tmpTile[index] = 0
                else:
                    tmpTile[index] = 1

            SuitableTiles.extend(tmpTile)
            tmpTile.clear()
        ind += 1
        if indexM % 10000 == 0:
            print(f'[{threadName}] => Done with {indexM / len(frames) * 100}%')
        # bar()

# file = open(f"{input('Имя файла результата: ')}.til", "w")
#
# print("Запись нот в файл...")
# for index, item in enumerate(SuitableTiles):
#     if (item == 1):
#         file.write(f"{index / rate / 2}\n")
#
# file.close()
#
# print(f"Нот: {SuitableTiles.count(1)}")


source = wave.open(input('Путь до файла для обработки: '), mode='rb')

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

p = int(input(f'Максимальный пик ({maxFrame} макс.): '))
tps = int(input('TPS: '))

st = time.time()

threadsCount = 5
framesForThread = len(framesList) // threadsCount
threads = []
for i in range(threadsCount):
    s = framesForThread * i
    f = framesForThread * (i + 1)
    threads.append(threading.Thread(target=GetTileCountByPicks, args=(framesList[s:f], rate, p, tps, str(i + 1))))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

et = time.time()

print(f'done with {et - st} sec.')

# GetTileCountByPicks(framesList, rate, p, tps)
# print (f"Пик 1500; TPS 3 = {GetTileCountByPicks(frames, rate, 1500, 3)} нот")
# print (f"Пик 2500; TPS 3 = {GetTileCountByPicks(frames, rate, 2500, 3)} нот")
# print (f"Пик 3500; TPS 3= {GetTileCountByPicks(frames, rate, 3500, 3)} нот")
# print (f"Пик 4500; TPS 3 = {GetTileCountByPicks(frames, rate, 4500, 3)} нот")
