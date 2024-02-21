from bimms.backend.BIMMS_Class import BIMMS_class


class protocole(BIMMS_class):
    def __init__(self):
        self._injection = []
        self._recording = []
        self.pos = 0

    def change_electrode_id(self, oldid:int, newid:int):
        for i, e in enumerate(self._injection):
            e1, e2 = e
            if oldid == e[0]:
                e1 = newid
            if oldid == e[1]:
                e2 = newid
            self._injection[i] = e1, e2
        for i, e in enumerate(self._recording):
            e1, e2 = e
            if oldid == e[0]:
                e1 = newid
            if oldid == e[1]:
                e2 = newid
            self._recording[i] = e1, e2


    def add_injection(self, inj=None):
        if inj is not None:
            self._injection += [inj]
        else:
            self._injection += [self._injection[-1]]

    def add_recording(self, rec=None):
        if rec is not None:
            self._recording += [rec]
        else:
            self._recording += [self._recording[-1]]


    def add_patern(self, inj=None, rec=None):
        if len(self) == 0 and (inj is None or rec is None):
            raise IndexError("empty ") from None
        else:
            self.add_injection(inj)
            self.add_recording(rec)

    def clear(self):
        self._injection = []
        self._recording = []


    def push(self, inj=None, rec=None):
        self.add_patern(inj=inj, rec=rec) 

    def pop(self):
        try:
            return self._injection.pop() , self._recording.pop()
        except IndexError:
            raise IndexError("pop from an empty stack") from None

    def __getitem__(self, index):
        return (self._injection[index], self._recording[index])

    def __len__(self):
        return len(self._injection)

class simple_injection_protocole(protocole):
    def __init__(self, n_elec=8, inj_offset=1, start_elec=0):
        super().__init__()
        self.n_elec=n_elec
        self.inj_offset = inj_offset
        self.start_elec = start_elec
        self.__generate_protocole()

    def __generate_protocole(self):
        self.clear()
        for i_inj in range(self.n_elec):
            inj_pat = ((self.start_elec + i_inj)%self.n_elec, (self.start_elec + i_inj + self.inj_offset)%self.n_elec)
            inj_pat = inj_pat[0] + 1, inj_pat[1] + 1
            for i_rec in range(self.n_elec - 3):
                rec_pat = (((self.start_elec + i_inj + i_rec + 2)%self.n_elec, (self.start_elec + i_inj + i_rec + 3)%self.n_elec))
                rec_pat = rec_pat[0] + 1, rec_pat[1] + 1
                if not(rec_pat[0] in inj_pat or rec_pat[1] in inj_pat):
                    self.add_patern(inj_pat, rec_pat)

    def set_parameters(self, **kwds):
        for key in kwds:
            if key in self.__dict__:
                self.__dict__[key] = kwds[key]
        self.__generate_protocole()



