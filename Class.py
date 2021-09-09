class Klass:
    other = ''

    def a_method(self, thing):
        print(thing)
        self.thing = thing

    def last_thing(self):
        print(self.thing)


k = Klass()
k2 = Klass()

Klass.other = 'a class variable.'

k.a_method('an instance variable')
k2.a_method(34)

k.last_thing()
k2.last_thing()
print(k.other)
print(k2.other)
