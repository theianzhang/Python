import math, copy, StringIO, sys, traceback,types
import Parse, StoppableThread
import GroceryBagger

_TRSTART        = '<TR><TD class=count>'
_TDFAIL         = '<TD class=fail>fail</TD>'
_TDEND          = '</TD></TR>'
_TDPASS         = '<TD class=pass>pass</TD></TR>'
_ALLPASS        = 'ALLPASS_XYZ'
_TDEND          = '</TD>'
_RUNSECS = 2

class Tester(object):

        def __init__(self):
                self.runtime = False
                self.resultReturned = False

        def doprint(self,p1,p2,s):
                p1.write(s)
                p2.write(s)


        def work(self):
                printer = open("results.html","w")
                percPrinter = open("perc","w")
                sprinter = StringIO.StringIO()
                printer.write('<html>\n<head>\n')
                printer.write('<link rel="stylesheet" type="text/css" href="topstyle.css">')
                printer.write('\n<body>')
                printer.write("\n<table class=border>\n");
                correctCount = 0
                count = 0

                p = Parse.Parse("input")

                try:
                        while True:
                                count += 1

                                a,b = p.getInt(),p.parseVS()



                                if a == None:
                                        break
                                self.done = True
                                self.doprint(printer,sprinter,_TRSTART+str(count)+_TDEND)

                                self.resultReturned = False
                                self.runtime = False
                                self.typeOk = True
                                self.eobj = None
                                self.result = None

                                def inner():
                                        try:
                                                self.result = GroceryBagger.minimumBags(copy.copy(a),copy.copy(b))
                                                self.resultReturned = True
                                        except:
                                                self.runtime = True
                                                self.eobj = sys.exc_info()[0:2]

                                #result = CLASS.METHOD(ARGCALL)

                                try:
                                        t = StoppableThread.StoppableThread(target = inner)
                                        t.start()
                                        t.join(_RUNSECS)
                                        if t.isAlive():
                                                t.terminate()
                                                t.join()
                                                self.runtime = False
                                                self.done = False
                                except:
                                        self.done = False


                                self.typeOk = type(self.result) == types.IntType
                                expected = p.matchInt(self.result)

                                if not self.done or not self.resultReturned or not self.typeOk:
                                        self.doprint(printer, sprinter, _TDFAIL)
                                        if self.runtime:
                                                sprinter.write('<TD>runtime exception:')
                                                #sprinter.write(' exception: '+str(self.eobj[0]))
                                                traceback.print_exception(self.eobj[0], self.eobj[1], None, None, sprinter)
                                        elif not self.resultReturned:
                                                sprinter.write('<TD>time limit exceeded:')
                                        elif not self.typeOk:
                                                sprinter.write("<TD>wrong return type: got <xmp>"+str(type(self.result))+"</xmp>")
                                                sprinter.write("expected <xmp>"+str(types.IntType)+"</xmp>")
                                        else:
                                                sprinter.write('<TD>strange error, contact professor:')

                                        sprinter.write(str(a)+' '); sprinter.write(str(b)+' '); 

                                        self.doprint(printer, sprinter, _TDEND)

                                elif not p.ok():
                                        printer.write(_TDFAIL+'</TR>\n')
                                        sprinter.write(_TDFAIL+'<TD>expected<PRE> ')
                                        sprinter.write(str(expected))
                                        sprinter.write('</PRE>got<BR><PRE>')
                                        sprinter.write(str(self.result))
                                        sprinter.write('</PRE>: ')

                                        sprinter.write(str(a)+' '); sprinter.write(str(b)+' '); 

                                        sprinter.write(_TDEND+'\n')
                                else:
                                        correctCount += 1
                                        printer.write(_TDPASS+"\n")
                                        sprinter.write('<TD class=pass>pass</TD><TD>')
                                        sprinter.write('got<br><PRE> ')
                                        sprinter.write(str(self.result))
                                        sprinter.write('</PRE>: ')

                                        sprinter.write(str(a)+' '); sprinter.write(str(b)+' '); 

                                        sprinter.write(_TDEND+'\n')

                except:
                        pass
                finally:
                        if count <= 1:
                                perc = 0.0
                        else:
                            perc = correctCount*1.0/(count-1)

                        line = '<!--PERC:%1.4f --><P>' % (perc)
                        printer.write(line+'\n')
                        line = '%1.5f' % (perc)
                        percPrinter.write(line+'\n')
                        if correctCount  == count-1:
                                printer.write('<!-- '+_ALLPASS+' -><P>\n')
                        printer.write('# of correct: '+str(correctCount))
                        printer.write(' out of '+str(count-1)+'\n')

                        printer.write(sprinter.getvalue()+'\n')
                        printer.write('</table>\n</body>\n</html>\n')
                        sprinter.close()
                        printer.close()
                        percPrinter.close()

def main():
        t = Tester()
        t.work()

if __name__ == '__main__':
        main()

# end of testerskel
