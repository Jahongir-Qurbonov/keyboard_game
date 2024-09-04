import logging
import random
import string
import turtle
from functools import partial
from typing import Literal


class KlaviaturaOyini:
    def __init__(self, min_tezlik: int, max_tezlik: int, bir_vaqtda_chiqish_soni: int):
        """Class constructori. Asosiy attributlarni tayyorlash"""

        self.oyna = turtle.Screen()
        self.daraja_chizuvchi = turtle.Turtle()
        self.oynani_sozlash()

        self.min_tezlik = min_tezlik
        self.max_tezlik = max_tezlik
        self.harflar: list[Literal] = []
        self.joylashuvlar: list[list[int]] = []
        self.harf_chizuvchilar: list[turtle.Turtle] = []
        self.tezliklar: list[int] = []
        self.bir_vaqtda_chiqish_soni = bir_vaqtda_chiqish_soni
        self.daraja = 0
        self.oyin_tugadi = False

    @property
    def alphabet(self):
        """Lotin alfabetidagi kichik harflarni qaytaradi"""
        return list(string.ascii_lowercase)

    def oynani_sozlash(self):
        """O'yin oynasini sozlash"""
        turtle.hideturtle()
        turtle.up()

        self.oyna.setup(800, 600)
        self.oyna.title("Klaviatura o'yini")
        self.oyna.bgcolor('blue')
        self.oyna.tracer(0, 0)

        self.daraja_chizuvchi.hideturtle()
        self.daraja_chizuvchi.up()
        self.daraja_chizuvchi.color('red')
        self.daraja_chizuvchi.goto(250, 220)
        self.daraja_chizuvchi.write('Daraja:{}'.format(0), align='center', font=('Courier', 25, 'normal'))

    def tasodifiy_harf(self) -> str:
        """Hali o'yinda ishlatilmagan harfni qaytarish"""
        harf = random.choice(self.alphabet)

        while harf in self.harflar:
            harf = random.choice(self.alphabet)

        return harf

    def tasodifiy_tezlik(self) -> int:
        """Minimal tezlik va maksimal tezlik orasidan tasodifiy sonni qaytarish"""
        return random.randint(self.min_tezlik, self.max_tezlik)

    def tasodifiy_joylashuv(self) -> list[int]:
        """O'yin o'lchamiga mos harflarni tasodifiy joylashuvni qaytarish"""
        return [random.randint(-350, 350), 300]

    def harf_chizuvchini_olish(self):
        """Yangi harf chizuvchini qaytarish"""
        harf_chizuvchi = turtle.Turtle()
        harf_chizuvchi.speed(0)
        harf_chizuvchi.hideturtle()
        harf_chizuvchi.up()
        harf_chizuvchi.color('yellow')

        return harf_chizuvchi

    def darajani_oshiruvchi(self):
        """Har 5000 millisoniyada tezlikni +1 ga oshirish"""
        self.min_tezlik += 1
        self.max_tezlik += 1

    def oyin_tugashini_chizish(self):
        """O'yin tugashini va oxirgi darajani chizish"""
        turtle.goto(0, 50)
        turtle.color('red')
        turtle.write("O'yin tugadi", align='center', font=('Courier', 50, 'normal'))
        turtle.goto(0, -50)
        turtle.color('orange')
        turtle.write('Sizning darajangiz: {}'.format(self.daraja), align='center', font=('Courier', 40, 'normal'))
        self.oyna.update()

    def darajani_yangilash(self):
        self.daraja_chizuvchi.clear()
        self.daraja_chizuvchi.write(
            'Daraja:{}'.format(self.daraja),
            align='center',
            font=('Courier', 25, 'normal'),
        )

        self.oyna.update()

    def harflarni_harakatlantirish(self):
        """
        Harflarlar kordinatalarini tegishli tezlikka
            ko'ra har 50 millisoniyada harakatlantirish
        """

        for index in range(len(self.harflar)):
            self.harf_chizuvchilar[index].clear()
            # noinspection PyTypeChecker
            self.harf_chizuvchilar[index].goto(self.joylashuvlar[index])
            self.harf_chizuvchilar[index].write(
                self.harflar[index],
                align='center',
                font=('courier', 20, 'normal'),
            )
            self.joylashuvlar[index][1] -= self.tezliklar[index]

            if self.joylashuvlar[index][1] < -300:
                self.daraja_chizuvchi.clear()
                self.oyin_tugashini_chizish()
                self.oyin_tugadi = True
                return

        self.oyna.update()
        self.oyna.ontimer(self.harflarni_harakatlantirish, 50)

    def harf_bosilishidagi_hodisa(self, harf):
        """
        Klaviaturadagi harf bosishlarni boshqarish

        Agar harf to'g'ri topilsa uni boshqa harfga almashtiradi
            va oynaga mos eng katta y hamda tasodifiy x kordinatani beradi

        Agar harf xato bo'lsa darajani 1 taga kamaytiradi
        """

        if self.oyin_tugadi:
            return

        if harf in self.harflar:
            self.daraja += 1
            i = self.harflar.index(harf)
            self.harflar[i] = self.tasodifiy_harf()
            self.joylashuvlar[i] = self.tasodifiy_joylashuv()
            self.tezliklar[i] = self.tasodifiy_tezlik()
        else:
            self.daraja -= 1

        self.darajani_yangilash()

    def harflarni_tayyorlash(self):
        """
        Berilgan sondagi harflarning tegishli belgisi, joylashuvi,
            vatezligi va chizuvchilarini tayyorlaydi
        """

        for _ in range(self.bir_vaqtda_chiqish_soni):
            self.harflar.append(self.tasodifiy_harf())
            self.joylashuvlar.append(self.tasodifiy_joylashuv())
            self.tezliklar.append(self.tasodifiy_tezlik())
            self.harf_chizuvchilar.append(self.harf_chizuvchini_olish())

    def harf_bosilishini_sozlash(self):
        for harf in self.alphabet:
            self.oyna.onkey(partial(self.harf_bosilishidagi_hodisa, harf), harf)

    def boshlash(self):
        """O'yinni ishga tushirish"""
        self.harf_bosilishini_sozlash()
        self.harflarni_tayyorlash()
        self.harflarni_harakatlantirish()
        self.oyna.ontimer(self.darajani_oshiruvchi, 5000)

        # Oynani ishga tushurish
        self.oyna.listen()
        self.oyna.mainloop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    oyin = KlaviaturaOyini(min_tezlik=3, max_tezlik=6, bir_vaqtda_chiqish_soni=2)
    oyin.boshlash()
