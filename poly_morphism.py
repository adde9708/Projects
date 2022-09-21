class A:
    def poly_morphism(self):
        def show(self):
            return print("Test")

        return show(self)
   
       
class B:
    def poly_morphism(self):
        def show(self):
            return print("Another Test")

        return show(self)


a = A()
a.poly_morphism()
a = B()
a.poly_morphism()
