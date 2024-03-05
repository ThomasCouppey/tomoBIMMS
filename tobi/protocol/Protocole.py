from bimms.backend.BIMMS_Class import BIMMS_class
from pyeit import PyEITProtocol, create
import numpy as np




class protocol(BIMMS_class, PyEITProtocol):
    def __init__():
        super().__init__()

    def change_electrode_id(self, oldid:int, newid:int):
        for i, e in enumerate(self.ex_mat):
            e1, e2 = e
            if oldid == e[0]:
                e1 = newid
            if oldid == e[1]:
                e2 = newid
            self.ex_mat[i] = e1, e2
        for i, e in enumerate(self.meas_mat):
            e1, e2 = e
            if oldid == e[0]:
                e1 = newid
            if oldid == e[1]:
                e2 = newid
            self.meas_mat[i] = e1, e2


    def add_injection(self, inj:np.array=None):
        if inj is not None:
            self.ex_mat = np.concatanate([self.ex_mat, np.array(inj)])


    def add_recording(self, rec=None, i_inj=None):
        if rec is not None:
            i_inj = i_inj or np.arrange(self.n_ex)
            if np.iterable(i_inj):
                for i in i_inj:
                    self.add_recording(rec, i)
            else:
                if 
                self.meas_mat = np.concatanate([self.meas_mat[i], np.array(rec)])



    def add_patern(self, inj=None, rec=None):
        if len(self) == 0 and (inj is None or rec is None):
            raise IndexError("empty ") from None
        else:
            self.add_injection(inj)
            self.add_recording(rec)

    def clear(self):
        self.ex_mat = np.array([])
        self.meas_mat = np.array([])


    def push(self, inj=None, rec=None):
        self.add_patern(inj=inj, rec=rec) 

    def pop(self):
        try:
            return self.ex_mat.pop() , self.meas_mat.pop()
        except IndexError:
            raise IndexError("pop from an empty stack") from None

    def __getitem__(self, index):
        if index > self.n_meas * self.n_ex:
            raise IndexError('list index out of range')
        i_inj = index // self.n_meas
        i_rec = index % self.n_meas
        return (self.ex_mat[i_inj], self.meas_mat[i_rec, self.n_meas])

    def __len__(self):
        return len(self.ex_mat)



class simple_injection_protocol(protocol):
    def __init__(self, n_elec=8, inj_offset=1, start_elec=0):
        super().__init__()
        self.n_elec=n_elec
        self.inj_offset = inj_offset
        self.start_elec = start_elec
        self.__generate_protocol()

    def __generate_protocol(self):
        self.clear()
        for i_inj in range(self.n_elec):
            inj_pat = ((self.start_elec + i_inj)%self.n_elec, (self.start_elec + i_inj + self.inj_offset)%self.n_elec)
            self.add_injection((inj_pat[0] + 1, inj_pat[1] + 1))
            for i_rec in range(self.n_elec - 3):
                rec_pat = (((self.start_elec + i_inj + i_rec + 2)%self.n_elec, (self.start_elec + i_inj + i_rec + 3)%self.n_elec))
                rec_pat = rec_pat[0] + 1, rec_pat[1] + 1
                if not(rec_pat[0] in inj_pat or rec_pat[1] in inj_pat):
                    self.add_patern(inj_pat, rec_pat)

    def set_parameters(self, **kwds):
        for key in kwds:
            if key in self.__dict__:
                self.__dict__[key] = kwds[key]
        self.__generate_protocol()


def protocol_from_PyEIT(p: PyEITProtocol)->protocol:
    tobi_p = protocol()
    tobi_p.ex_mat = p.ex_mat
    tobi_p.meas_mat = p.meas_mat
    tobi_p.keep_ba = p.keep_ba
    return tobi_p

def create(
    n_el: int = 16,
    dist_exc: Union[int, List[int]] = 1,
    step_meas: int = 1,
    parser_meas: Union[str, List[str]] = "std",
) -> protocol:
    """
    Overload of pyeit.protocolcreate 
    """
