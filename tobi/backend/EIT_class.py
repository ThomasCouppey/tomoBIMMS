from typing import Any
import time
import datetime
from json import dump

from ..protocole.Protocole import protocole
from ..results.EIT_results import EIT_results

class EIT_class():
    def __init__(self, N_elec=8, protocole=None) -> None:
        self.N_elec = N_elec
        self.eit_results = None

        self._protocole = None

    @property
    def protocole(self):
        """
        
        """
        return self._protocole

    @protocole.setter
    def protocole(self, protocole: protocole):
        self._protocole = protocole

    @protocole.deleter
    def protocole(self):
        self._protocole = None


    def update_injection(self, inj_pat, **kwgs):
        pass

    def update_recording(self, rec_pat, **kwgs):
        pass

    def get_recording(self, inj_pat ,rec_pat, **kwgs):
        pass

    def eit_measure(self, inj_kwargs={}, rec_kwargs={}, save=False, fname="output.json"):
        self.EIT_results = EIT_results()
        date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S/")
        self.EIT_results['date'] = date
        self.EIT_results['protocole'] = self._protocole.save()
        self.EIT_results['status'] = "processing"
        self.EIT_results[1] = {}
        t0 = time.time()
        try:
            for inj_pat, rec_pat in self._protocole:
                self.update_injection(inj_pat, **inj_kwargs)
                self.update_recording(rec_pat)
                self.EIT_results[1].update(self.get_recording(**rec_kwargs))
            print("injection done in ", time.time()-t0)
            self.EIT_results['status'] = "completed"
            #self.EIT_results['comment'] += input('optionally add a comment:\n')
        except KeyboardInterrupt:
            self.EIT_results['status'] = "Interrupted"
        except Exception as error:
            print("An error occurred:", error)
            self.EIT_results['error'] = str(error)

        self.EIT_results['duration'] = time.time() - t0
        print('duration:', self.EIT_results['duration'])
        if save:
            with open(fname + ".json", "w") as outfile:
                dump(self.EIT_results, outfile)
            print('measurments saved')
        return self.EIT_results

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.measure(*args, **kwds)


