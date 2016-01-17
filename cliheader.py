""" An extremely simple interface to display a title when starting a python script in a command line interface.  I'm only formalizing this here so I don't have to rewrite it, and so that I can consistently format my Python script outputs nicely. """

class cliHeader:
    def __init__(self, title = None, version = None, author = None, whitespace = 0, bars = False):
        self.title = title
        self.version = version
        self.author = author
        self.whitespace = whitespace
        self.bars = bars

    def show(self):
        print '\n'*self.whitespace
        if self.bars:
            print '-'*70
        if self.title:
            print '|', self.title
        if self.version:
            version_string = 'v.'
            for i in range(len(self.version)-1):
                version_string += str(self.version[i]) + '.'
            print '|', version_string + self.version[-1]
        if self.author:
            print '|', 'Authored by:', self.author
        if self.bars:
            print '-'*70
        print '\n'*self.whitespace

    def show_terse(self):
        version_string = 'v.'
        for i in range(len(self.version)-1):
            version_string += str(self.version[i]) + '.'
        version_string += self.version[-1]

        print '\n'+'-'*14, self.title, version_string, '-', self.author, '-'*14
