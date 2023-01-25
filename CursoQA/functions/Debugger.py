# -*- coding: utf-8 -*
import os
import json
import ctypes
import sys
import tkinter
from tkinter import *
import functions.JiraConnections as Jira
from functions.Functions import Functions
import yaml

current_path = os.path.abspath(os.path.join(__file__, "../.."))

class Debugger():
    def __init__(self,instancia, entity, incoming_exception, json_GetFieldBy, json_ValueToFind, complete_path_json,  json_strings,
                 nombre_caso):
        self.instancia = instancia
        self.debug_this_entity = entity
        self.incomming_exception = incoming_exception
        self.json_GetFieldBy = json_GetFieldBy
        self.json_ValueToFind = json_ValueToFind
        self.path_json_complete = complete_path_json
        self.json_strings = json_strings
        self.case_name = nombre_caso
        self.send_this_code = 0
        # fuente
        self.unified_font = "Arial"
        self.stored_images = {'back_btn': b'iVBORw0KGgoAAAANSUhEUgAAAE4AAAAfCAYAAABJePtPAAAACXBIWXMAAAsTAAAL'
             b'EwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAITSURBVHgB7ZpN'
             b'TgIxFMffoG5IjC5YqFEy7uQEIqvhDJIY7mCCCQcw7iXCCVyywTMwK5AT4E7CQk1k'
             b'zRb7yryhlGGQhiKR90uGfkA6vH9f+6adOhDQPXI9cOBeZD1govBhBA+Zr56PBQc/'
             b'usduUyReqlwCZj6DSg0TP/PZyzuBpzXTjTokc1lg5jNsvUK/UAThefmd2/3DZ+Fp'
             b'7sFNAZh49s5OZTpsd9wE8JxmgpcAxggWzhAWzhAWzhAWzpCNFG5Qqcpnpk3GinD9'
             b'6yK8nZzPGI91eC0Cn9CH7S0ULpm7lKlqPImYvPofq5NdsECqfCe9Bi/MIyRiKKoQ'
             b'UhUWBdWXfPQb+m5eWb0vgkNd/z+rxopwCBqnGhUskEMj5JpPlkvBdzW4+HifaWcs'
             b'PoyFEu1hOd3IhutG8mC6F3Waig3hrAUH8ix1oqfdF/II3FhAozBV6ydtZIP62lSK'
             b'9ZRPv9TlhQLqgmFHRHXGKrAmXDhEW53JMNXmNxImbldG3+qiMrVJAWfdwcTaUEX0'
             b'4Ro1h9FcFdcGDmOKxrr4f7WHaPU5To2uqoFk/DiAVCdDMCLiorBqPYkfep7waELN'
             b'28aqx6kTtW48BQXyyLiNVOwAXXxsm6YBtY21IbbNR9+PTyPmd6BWqBmvVQ1h4Qxh'
             b'4Qxh4Qxh4Qxh4QxB4XxglsXnN/lLoL7J57MjSzB1doQq+bTSQqZOK/0A8eQsLE8x'
             b'esUAAAAASUVORK5CYII=',
                                      'exit_btn': b'iVBORw0KGgoAAAANSUhEUgAAAEQAAAAfCAYAAABeWmuGAAAACXBIWXMAAAsTAAAL'
             b'EwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAHgSURBVHgB7ZnN'
             b'TsJAEMenqBcSowcOapTUmzyBH6fyDJIY3sEEEx7AeJcoT+CRiz4DPfHxBHiTcFAT'
             b'OXPF/rcM0JGgJGxr0vklMO2m3XT+nZnd7To0obfneuTQbXDoUbrwaUx3hc++jxMH'
             b'f719txkYL1etUBoZ1uowfuGjX3QmkdHMPzcoe3FGaWTU6tCgVKYgUoob19u7T0Fk'
             b'uDtXJUorW0eHxo7aXTdD6asZy/AypERQQQQqiEAFEagggn8nCOYEw9ojJYU1Qcxk'
             b'57JMrwfH5odjtP16X7vDM0cjDO6NU6BNsoSZ+QXwcgBODkodOnl/+3MfueqNsdnz'
             b'+GbQ1gQBcGTeKbx9RAmWCLA4Z/i6eWREIVK4H1gbSw1rgvCDsxN4eHaA1w5h+6mJ'
             b'nlGrS/mXRqQPTp9clcy9YSqF6cRt68ZaDYFzcDhMlfKPGoJUwjUcGfPRsgz0ibRb'
             b'FFHrwOooA4fDh68YhyHMLGW604K7Cogom1gRRI4OeJtcXDmNYPHJYZUiGwdWaggE'
             b'QKrw8AkQEYBrC5PknGMR1ooq3r4UBVEyK4T16dAsRUqU4PPh+Ov+YZx2oAG00LWM'
             b'QAURqCACFUSggghUEAEE8UlhfN25o+jOne7tktjb5Ubd/Q93/78B5bris0YF+zQA'
             b'AAAASUVORK5CYII=',
                                      'input_text': b'iVBORw0KGgoAAAANSUhEUgAAAcwAAABDCAYAAAARSjU/AAAACXBIWXMAAAsT'
               b'AAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAArFSURB'
               b'VHgB7Z3Nbhy5EYCrxzO29Rf4YEPRJdDBF599CXIIJu+wNrDJwY9i+GGCHJR3'
               b'iBAEi32DXHwwclEM+WBEHtn6WXVYPWSruqbYIx3X831Aq5tsslgskuKQzWY3'
               b'4vj3bw/n0sg/BAAAYFNp5U8v/vvh2HpNXZBGO8vf/f1vsv2H3wsAAMCmcf7T'
               b'z/KfH37UgeNEtOvMqEPati3XD/SCzhIAADYV0wdqv9hYhzQJPR0eHk4FAAAA'
               b'5Pnz59P5fP6guLsOUkeYqc988OHDh5kcHAoAAMCm8/79+1k6dApWB5c33Qjz'
               b'9evXk+zBCBMAACDx5MmTaRpldjOw6u46yKOjI3VM9vb2HggAAADI58+fH2xt'
               b'bWm/eK3uibnXnJ2dTQQAAACUyc3NTTfCTI8um0GHKWY1EAAAwIbTfPz4UZ9h'
               b'tro21naYrZj3TQAAADYc2ye2pcNkdAkAADDE9o39lGxrbgIAAEDqG/f392U+'
               b'n2vf2PavkSTPNs3VCgAAAIjs7u7qM0zRoyz66UaVdJYAAAC3fPnyRQ4ODvr1'
               b'PWVj2c6xs7MjAAAA0I0w5eTkpDzHXC76efnyZXdeLBYCAAAAyxGmpeso9/b2'
               b'eJ0EAAAgRvvI5SrZ4+NjPbFCFgAAwKCrZJV+44L5fC4AAABwS3qG2b09kl8r'
               b'EfaOBQAACCjPMNMsbL9KtkzJKjzLBAAAkOUq2Twle/t5r0wrPMcEAADoSCPM'
               b'powy27btOsx+nzwBAACAQrc13osXL1YX/bBxAQAAwBKdktVFP+WxZbfTz9nZ'
               b'WTe6XCwWPMMEAACQysYFBqZlAQAAlnR9Yp6F7bbGa8xOP4wwAQAAlnTPMAdT'
               b'sua1EgAAAJDbz3tlGjsl2+oDTgAAAOjoZl11SlZfK7EdZuMfcAIAAGwq+h6m'
               b'nu2UbP9AUwAAAKBD95LNl7db4ynPnj1jhSwAAECmjDCl+1hJc7uX7OnpqQAA'
               b'AMCSspds2dyHvWQBAAAC0giz1bU9ZaVsPyWrvaiZrwUAANho7JsjfpWsna8F'
               b'AADYaMqbI69eveoX/dBJAgAArDLoH7udfvTC7GYAAAAA5nXLfpVscQvvYgIA'
               b'AAw4OjrqRpp8rQQAACCm7xPbhN9LlhEmAACAQd/D1J0L/F6yjDABAABEVl61'
               b'nAgAAACsUF4rYfN1AACAEfR7mNbd7yWr7OzsCAAAACxHmLoLniwHlINFP7JY'
               b'LAQAAABWn2HazddZ8AMAAJDRhbD5OebKe5g8wwQAAMiUzdfzOp+mX/ST52kB'
               b'AABAVlbJtv2iH/aSBQAAWKV8QLqfkn327BnPMAEAADJl0U8aVOq56T/vdXp6'
               b'KgAAALDE7H7XfZykf4aZRpgCAAAAIU33WkkebgIAAEBGV8mWhT9t2/YfkG72'
               b'9/db4dUSAACAjtJZKuUD0t0c7cePHxth8wIAAIAOu9NPGWGGNwEAADaZsugn'
               b'fw9zuNNPuXn+088CAACwifg+sHygRBf9DEaV/7y6+Msff/jxrwIAALCh/Ovq'
               b'8s96Pjg4aE9OTrop2fLMcrq/v/8oPcfU73v9Zjab7V5dXW2l69l0OpXr62v7'
               b'bLN7H0XPek+v0/2lkNuwrQ1b/NPZh7XyQlK4JqcxkBXF0bDpXmtkS3SdZQ50'
               b'z/mx7nW6NU62j1viF1on05+9vr199Y+x31jeOz00bpZh07wp+kS2j8rI6SiR'
               b'vuLqg9pfjC1zHkoZRjq3RXdnq+h5elvRU5xeo+UW3FP3xOgf5V1snoKy9vXf'
               b'1teiexPYdlT/Sn33daak11j9S30xthqkYduvbee2nplrnzbtn/Y/CPOdtP9f'
               b'0vVVOr6l4ywd/0vHeTouUof5S1HqQToepWP78ePHe9++fdtJneZ26jSnsmqs'
               b'KsE/HH/Pnm3B+vj+n1RUuZog041Pz8qwaQcN2+ox0K2iV/hP0+nTy3Yy2uCH'
               b'iNxBtq8wTWCfSN/SKKy9B/84ff5cPpqRPPpGuJJXqdehMH52+3/yoSyf/9II'
               b'gzRso5Z1+Ppay8dI3fDpDf6RRLo4d7XjNvZpgrASdHJhGkF6fV24xz8xCfIt'
               b'Qvun/f862792mNcPHz78enl5udjb2/tydnbWdZjpuLEd5kNZdpq6Pfu2XqdO'
               b'c5o6zSYnKMndqjudO0Xy9U06T8o9r2Tyb5J/59Z46brcl+zu4wTuEldy/E5O'
               b'ltHLsfrJaoGUNG36EhjUyyxyre4+H2Ly3Rode4J7A3tkOw7Sc3aQin2s7q3L'
               b'W//PwPiHFa/oYOJ5G/W6O/k2nuSykkA3b6dBfow9etnG1oM64urPQHbJV1DW'
               b'tcZm9R7YqviVPFXqndWpdbqX/PVl7WxpbRzVc8np23q2Yidryyhtaw8JOodS'
               b'V6O6JsMyp/3T/jel/d+kzvI6dZYXW1tb51+/fj0/PDz8+ubNm8t3794NOsxJ'
               b'mpZ9mKZldSr28aNHjx5eXFx0/ula0rWUs0+0KKL3FRe2UzS7V5R3MtXdZnfj'
               b'/MJfP+leU+JrOI3n0pEoraxrkbsix6fn/bysQO4gDxL8UnM2CdPI9vT5Kfcb'
               b'Xx7qVzwCuzaRHsavt0NJu8iN7G/19eXo8tiHl2X5yF3iFPuYfNZs2F/7vNfS'
               b'iNLJ3o3X09lokA9b5wPZNVuXdKK4gzjFxiVNua2zY+n1deEOdrBlL6Y8+zpM'
               b'+6f9b1D7V/f1ZDK5TJ2lTste5EN737YkrmddMatTsLN8THd3d/XjmeVdTRXY'
               b'7uzsNIvFYpDw9vZ2k2jVX6/Pz89biVkpdOuXZHdGSXKa4laZtXNJV8Mmt9Wt'
               b'ybpKllWux/TocWEl0mUMa4O7hPdhsh3kDvYM43h5WYb6p2n4ti+rzIotbF6z'
               b'zMEvsxG7rsWWnc9XSa/kwxA18kHexOShVtbWRvfByGsiG0Z1o2YX9df4Je/F'
               b'Dio32/TedXNduKA8vf3DNG2+hfZP+9+M9q9h9XmvzttqJ3n16tWr66OjI/Xr'
               b'O0zJhtTOsRtVHhwcTE5OTkoDXkH3nj09Pa3+eg78myDMyq/UJLfVjeCfPn3a'
               b'fPr0Sc+i5yIj3x+EtfqY8LV0xaU/iGPkt1mHNsvu49kwJW3FpF/iehuIl6Xh'
               b'tQKr/dVD41r/HLZPS+V2Hst7/hdsCStBfI+vhL19TH68rSL5g3tqm2ILGU6H'
               b'iKyvA1LymO1gw9gyj34pt6ZORr/IfZ0JwzkZK24x9aXICtLtdZI1tq/oY8P1'
               b'9tBzKVNbv7wM1zajeteFtW2p1FuJ7bwC7Z/2/x23f+0cu2M+n98cHx/f5DAr'
               b'upaRZhlt2mPmjmkSVvwHYV6+fDkz/rMR/+6scipx+vslvXJdwhd3Rc8+HSO/'
               b'989+Ud58nnz8mXd7vZ1sa6t1cmo6TddcTwP/MbvWdLPxepsXt56tTG9Xb1N1'
               b'mzKaBWlFdaNaJrW6ZXVck0Zkh6qf07+mV5j3MV3E1cOgfvi8DsrCtT2blvef'
               b'uTZT8w/rhtD+o/i0f/mu2383aNTj7du3E32d5D74UWZ03Yz4j4VtKmk1FT3u'
               b'Ij9Ko5ZeLY0ozl10a0b0kIpMqaQ5FqaW75pOIncvi1oea2lE4Wt+Y/ejsGO2'
               b'H0u7Jmed/Ej2WBmuq4dSSbemQyS3kfG6sS6eVPzuW8Yi43lYZ/d1dot0lCD+'
               b'OvlRGnfN81icu+hWs3kUTuT+Oo/VxzGdRO5eFrU81tKIwtf8xu5HYe9Tn33c'
               b'SM46+TU5Pf8HSxm/zYiCs6UAAAAASUVORK5CYII=',
                                      'refab_btn': b'iVBORw0KGgoAAAANSUhEUgAAAHAAAAAfCAYAAAA/QknEAAAACXBIWXMAAAsT'
              b'AAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAALpSURB'
              b'VHgB7ZtNbtNAFMefC2wqIVh0QRFU7o6egNBVegYiod4BqZFyAMQBIiUnYNkN'
              b'nKFe5eME6Y4qC2CRdbbF/5l5zniYJKWtHT/p/STX9nj85uM/783YjRNyzF6l'
              b'bUroS37YJqXJZHRLX0/+3GQ4SfBndphe5bv2Qe+ClOaz6A+xy05+35wlzvOu'
              b'jr5f0v5pi5TmsxxNaN45p9wTz558fv7yW+556YtPHVJk8OztG7NfjqfpHumc'
              b'J5n2HimiUQGFowIKRwUUjgoonKfUUPCssxxPaP9DS59PN1CZB16/Pv5nW/QH'
              b'd7qXH1TxxgEi7gLUFXVGXZpM5R7Ir+eWoym/AsrTuhvvYdEe+nYIAqD8beXF'
              b'gOcf9Kjx3l+DgK7zeuRG9NQcA98jOVSa0Ik8tBIS6aH3+qLE7HCaGTg0MPk5'
              b'LEfLDNJ9wuthHda2I1LWY1PbHBiGIjQaHsmdhWN4XIwwL3cMOnD+8byYK236'
              b'ejvm/SHZqGCjwZDe/fpp7uPoYK9TUScjfHAdmLrk+bj8u9isQsDKV6HofDTS'
              b'7zybbgU5+nFptiLtFCP1vcvbLRqN+/y8DIuHdHQcp7F3wBaO2UsgLs5Z5NB7'
              b'YCMMuThHOts3dlw9YJ9trtq23eZjUesqFA30RyE6GmHVP4+BToC41/3j+HUn'
              b'OPA7OZ63VdqvsxMDAxGEHs6Dc1vdqqByD/RHJs9t5esXpS0Gr0ZDL4jnHWxc'
              b'OfK1/11dGrsuVPricySxXlb//1Nr8UA0mOcIdJwJk8WcZYG46zqA88UWE+yd'
              b'jJ23Vh7Gixg7fw5th49XC6WwHtHyR5OgjEFxr58nNkCrprYQauehoQk3GK2Y'
              b'QxCSuGPClZ8PQhbuw+Yveti7F30q2SnmPyeO9d5uYSd8TNkqoHfdFxI2uYx5'
              b'ZzfPi8nsML2977OSsjt4Za7vQoWjAgpHBRSOCigcFVA4KqBwIGBGilQy/WW2'
              b'QPxfZuu3EQIpfRvBifp1khhKXyf9BYiBwemnPkn7AAAAAElFTkSuQmCC',
                                      'report_btn': b'iVBORw0KGgoAAAANSUhEUgAAAHAAAAAfCAYAAAA/QknEAAAACXBIWXMAAAsT'
               b'AAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJDSURB'
               b'VHgB7ZtPTsJAFMZfiQu7xJW60cTExAsA7uAUbPQIJHoC4wkg4Qi64RR0J3AB'
               b'EhMT3KArWMIO55v2wVD+1Q3M0/dbkM5MX9vMN997FNqAEvqnl2UK6Mlslknx'
               b'mYhm9HzzPYjQCPDRP7tskwonjejma1AJEue1SZHHjCq5JG0qEjHaBSZ9zkgR'
               b'S44U0aiAwlEBhaMCCkcFFI4KKJwjOjBXn+8rfaN6k8aNJim7ObiADEQD4W2B'
               b'Th5rdnufIvJC+ri4Jkl4IyCLNW6sujL/UJtvTztdmnR68360j0vFlbGscW48'
               b'j/G1ZI13z7lvvBGQCUuFpfZ568X0Fc0kdW0b7hxW7+ykxU6t2bHQirAYc+PS'
               b'YxwHRvX118HxyAycFTbFq4AUr2pMVOi4CbAIw+q9bcOdx7YvnjSulxD+vPU6'
               b'dxNPPrsJcXkz8ZPkOO4xQTptT956NDbx8Xlq9njuedPxh8I7BwJe6Qwmz02r'
               b'mOx0feT9sQg2ETqpEgJtAwsIC2ITu+L3hVc1cNoxDmwVl5wCsNqzTti2/TgN'
               b'ZwHiscuQHdihvuHVfSBcxDWLa+GihsXAYVNHCLQxwahZDLszPZZlEbhfXOwx'
               b'zHVsc/Wh8e5GfpzcTuS5Jtk61LUO2OQC9HOtZPGQhtG3bmwd2J+PBXjhbEuj'
               b'PiD6/0DUxf9+068/pQlHtIBw3/QXX0z+IvpIhXA0hQpHBRSOCigcCBiRIpUo'
               b'h+fsSZGJ0S6XvCQRkSKNCNrZGoiXJPCcPamQEsDbSRWrmeEHHQ8+Wz/fr/gA'
               b'AAAASUVORK5CYII=',
                                      'retry_btn': b'iVBORw0KGgoAAAANSUhEUgAAAHEAAAAfCAYAAADQgCL6AAAACXBIWXMAAAsT'
              b'AAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAKASURB'
              b'VHgB7ZtPSsNAFMZf/AN1oagrFcGAIHiBqrt6BUHc6A0s6AnEEyh4ABe68RTN'
              b'zrYXKAhC3VRXdtnuar6ZvHYSG1rb2nSG94M2yeTlZZhv3szktfEoorbhF8ij'
              b'm3C3QMKsE1CHbve/6gEOPHzVNv1SuCmsXRVJsIPm/QM2wf5n/diLIrC09fJE'
              b'S4cHJNhBq1yhxtkFhRF5PH+5vPoYRqC/cnpCgj0sbm+rbbtS9edI5kDbKcyR'
              b'YD0iogOIiA4gIjqAiOgAIqIDTF3E95292Kdxdq4eXAfxffeg7LEV4mQWiUjx'
              b'4dMqV1XmYZCQ69fafukoP8h1V/BxmZSf/2aBMgKiMMgDtl6r3bSfGW0QDeVJ'
              b'kWGDc7jO9Am7dmQLG74PypO2o/jpV7ekH7N8GmQmYhp6eIWgebVt3hMhr4vG'
              b'0Unfomog7OMc2zH9IpXzjLDVx9oewph+zHP9/HDdMCJAYFzLOWf2oylOVcTM'
              b'hlP0XDRKlI3v9n5upK2XZ9VAwIwSE7bb/XjrlqHxclEDcvSoRDFR5PNZ7fN9'
              b'9TX52Lk0PzjGPXHMtmbd4Ad1MUeZaTATkcgicIPoXj35BUza/JYbMmoQnegQ'
              b'aXXLZfQrUKZzYqscDoVho5hzDkCPNhskOWeNyri/l3JEc6eblUVPps+JGLIg'
              b'mFrYhENpbxHSE6w9xONHGugc8MvznelzmFVu0g+j59hzmhUyf9hfi4RrRqs+'
              b'ngfNIfWviwQWiFe9mL+4s+gOM1xU//aj68YRCcbpZJPCq236HZ6sBbvACIEO'
              b'Jmk3BxARHUBEdAAR0QFERAcQER0AIgYk2Ewg/wC3FPMf4PIuhqXE3sXgQnkr'
              b'yipib0X9AHR/VtukMGVBAAAAAElFTkSuQmCC',
                                      'sad_face_img': b'iVBORw0KGgoAAAANSUhEUgAAAGIAAABbCAYAAACI0FBrAAAACXBIWXMAAAsT'
                 b'AAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAA74SURB'
                 b'VHgB7Z17cFTVGcC/79y7m0QIYHjthkd2I4EkECyVjoitgqMVWqdjtb7Gqa1j'
                 b'O2r/kE5pK+NMK3ZaqqXTUewTO3UqDgo+Rmd0pFYgQouiCIOBBCXkBXkRwqME'
                 b'kk32nq/fudlgCHvuvpMQ7m9m9+7uOffuvec733fO+c4LYZhT5Qs8ft4PCCvj'
                 b'OpHOj1fSUvcEDGMQhhGc6Iv4cD3flTougsxQzkIq5+P7LJxyGCYMuSDsHJ/Z'
                 b'hI+FLZih1pghEUS/nL8ShhO95mxINGVQBZFM7ucbtPjQTgSH+MtBIqwWQjZy'
                 b'SLsEcUZIOIlAwhI4BsjK5c8T+OtUQJrBcYo4dYN8zONrCIifQdeSQRFERAAr'
                 b'Y0TrUlH5VcGJ+Tm/GiSJw2D0VLzc2HiCU0RCEhA/Y3XejFwru7uMQEyXhIUC'
                 b'aDYQlbFsZrHAPDEusHIwBJJRQdgmCGFrjGgn+Cb2ScB3SVKFRbKi7GhDLdpp'
                 b'mH42Ahhz84MziOQcICzj+1vCP5fwa4zjiQSLM2myMiKIiABUtXORJgonMrXz'
                 b'3+9BwG2WtD442trw/mKAMAwi+6DUa/rP3kAIC1hDruWf5vE9jXc4RZmsJzIh'
                 b'kLQLIpYZYgkcRYIP+dN2tto7TnV59i04Xv0/GEIOXV44tjM7XGaiuJbLohv4'
                 b'p/n8ytOekAFzlTZBxKEFnOngQ4H4lgT5Tk4WVgbr6rpgGLF38uRRXsqeCyYu'
                 b'4cReyj99xSF6WrUjLYKIWRYQ9nChuJn/7Jkcj9xZ0NBwAoYxVVOmjAfyLuSc'
                 b'8xP+eh041bjSVHakLIgqf0AJYJFDlDb+k5e4mrm+qLXuo0wVwumGb1Ic8AWu'
                 b'Q4S7ubp2J9/35Q7Ry0ua6xZDCqQkiFhC4CroupDsevjK1tYzcBFzMG/GGMsb'
                 b'XsuF+l0O0VISRtKCcBKCaoRxefAAq+w/YQRRmR94lCsavwV9uiUtjKQE4awJ'
                 b'2M3lwfqSprr7YQRS5S94lavct7LpMjRRkhJGIs3+yI04akInkHzOA92/hBFK'
                 b'j0U/l0jP88eQJsqiSBolREIa4SQEAjrLb3/qgtDqL7e0tMEIpiI/f5qHvI+x'
                 b'3+sBBxdJQpoRt0Y4miOungrAFyzR8+xIF4KirKnpsCcc/gOh3AB6H1hCmhGX'
                 b'RsRoJ1Tya02PR26cO8zbB+lm38SATxhwn0B4kMuMwqiR4mxnxNQIRyEQNHHt'
                 b'aIMVhjcvNSEo5rTVtQDiBiJ6nRPjWNRInHaR/hdHYpsmhxYztxPeMRA22jd0'
                 b'iVLaXFsvBazn8mKLNhLClljXcRSEo43jcoH9Fi/ObK77HC5xSpvqK5Dki6Av'
                 b'LzBWeaEVRESdFunCWRv+fdoM78QkO2xGEpwG4a6Q2M41xx0O0RY5mSjhcPXN'
                 b'uiAuF1otC59ceORIJ7jYzDtZd5LLzCf5pXfpI/xLFxRVEJGxRDohsUkUt8xu'
                 b'q90OLudR2lL/NrcrHnaI4r1gnFaEqNVXtmd6DynBy1wduwdctHD6lYMapaKB'
                 b'G3oXpPsFuV4nMQVLx0KBK8HFEZKwwik8WhpfaH4cujnZN7+uuKn2M3BxpLS1'
                 b'jruCYZs2QpQ0Pk8QTtrAkCB4Clzight5jmk1MK3x/MBgt86JxX74zcUtdTeC'
                 b'S9wc8Af2sDn/UvRQ6ihprs/t+3ZOIyomBec6eBJPWyCXgUtCSMBlkZGKUcDR'
                 b'B/KDs/q+nROEIeTXdBfksuHjjS0NVeCSEGehaxcfDurCSdI1fZ/7lRH4tPYE'
                 b'wDeecFvQCTO/uVn10bypjYCwpu+jLYhKf7CAc70ZNTJB2CtwE7gkiXgN9CNX'
                 b'cmvZlW7Hst8kXKm/ELR9cqSmBlySwmgRn/LhtC68y4Bidew1TcKxqlV3p7bA'
                 b'cYlFEVSrvu0j2ggIdv++LQguAwr18eAwuKQEp2G9Lqyveivs4YVA3qiRuHyg'
                 b'3q5QlxSQRPt0YWoE4b6JE0cL6DFnOlyjnSO2gktKCEDVjartMsgycqYLQ+iH'
                 b'n3On+HFJcMn1RacbiXSc7ctxXXg30niTkPJ0gzlIzeYRmJQg7CHuImcVX+Mm'
                 b'9lE1cdXs8eKmhv8OjFcbCGR3heibfA9qKONRrkavLm6qexMySKWv4BsCcQXf'
                 b'2zhCuby1qWFrtEkylf7ArZwyypOqBiBv6sqCx+fVcQdQgvA1jnPXcjt/mBI9'
                 b'3BhvShLLdYNq2HF1UoCVlCA8IucVPixVlyaEEnYZLq7yB5e2NNduUQ/NHi9x'
                 b'x6QpZV3dtAwJb+M4YzlqEZdLCyvzC79e2lTzHmSAA5MLbiDEt6gv90mxzucL'
                 b'/KVC4l/LjtbaZtguN6X3Nr7ztf1OnZkdAuWSWAKJQnic/02bjgj4A9YIyNMP'
                 b'bsLTiIa2DqyD/VaTuU976YCfuYZGb/v8gXb2lahcNZpfE1jtsuj8G0DuiP8Z'
                 b'HzMiCBaCujZ+8WcwmQ8rTYOWc4dOG+c+yb0uE9nvFm1O3c1qLFOio1YQrA4C'
                 b'0QH6HJ9nYm+CRL8AQihkyW5IEI88fZaM0WrE38QBQar1PjnycqIWMgQ/0wGK'
                 b'nqtz7Rc6jrk7mRMWiffTS7MbDArpI1Au51Ic5RChmzxWwoKYdexYB5ubZ0HZ'
                 b'xoSh3WBRxobzW0gv8GFH4mfCSTabawtP1CQ83w8N6mbN16cj4mhlLpzmGVNW'
                 b'SCTs7FOzgsjo/jObnN/xDVTEd5aaZQrrudK9svho/YeQIWY31e/hO2QfJr1q'
                 b'D5yOQWSux07++BS3qp5OZsaTFQ5bbOr03gkCL5sK7NE36NCwPB4TkqCksbH9'
                 b'8NSpazrIqGZtX8oPs4ALpeL+8wrsh+zVmiqS+Dpa+E7JsYaMD1graa59d79v'
                 b'eiPXVj4FlHfxnQT558sGRFNC+piFtYtrWO81Z0H54ub6pCZfGqZpcDPAcBhp'
                 b'HOJEJjWtKqoglEfWlJYBSTKtd9zTaxX5+R8JMhfwA83jB5vAAsliIfeQrQXU'
                 b'wNXbquLW+vLBHKw2u6Vh/0GYUW35rAOsuUWcK33ccOrtMZN4hp+9mTsMdnSE'
                 b'jN3zT9ScghQgC71kUJZD6dNhco7s0E7UY5XhHiMvpIgaxs6Hw7v8/rdHm+a4'
                 b'7hBm53i83aHuUydnt7WdSUbd04HtkGuBV7ZyJcI3ZcpYsDy2IAR6Ok43556a'
                 b'D5/0QDoQYS+CSkeNKBBOm9wXreq40zQR8igs9RO/E8TuKOlV+WGF3ZhjU8of'
                 b'2yEDsFVSNVNt7ZTLj+NsLeTvHa4wxjJwLLikhvJekMNKBhatFVK1+jSo1i63'
                 b'+JwXC3GJCanlJGxXUnS4FD4uwEEQbNEmSJATwSU1CMdj75pRUfGQaBdo9hx0'
                 b'uMQEgcIPLinBuX08a0WOLrxLdh4WJb2FlK7Vx2W5nAUuKcH+rTKH4Da1MkOk'
                 b'q5QO6WKxSk0Hl5RgE1/gEPyJerMFgZIe1cVilQoSQFKtaxeArdzfwuk3VRfO'
                 b'rt5V6mgLwivMvQ7XGn/QX1AELkkxqdMeqqRtQ0jLtF06tiCuaK5psNdUig57'
                 b'IDDxzhAXG+5cuR00TWrVA9rXGSW++FH+WHcxCXS7a54Sp9HvvwwRv6UL5zR/'
                 b'pO/zOUGwl9ZhThxeVe0vmAsuCXGKstRSdFqznhWW59z95wRR0nqkwl7iJzrZ'
                 b'YUC9K8TlAlSfOJulP4J+UuiJGW1Hqvu+nB+JaBXo4c7/6VeBS1wcmBxUI1Pm'
                 b'aCMQPNP/6wWFiOOMUsDXuFPlO+ASkwP+wDZOSO2ck4EzSy9UG3JaOpq+vc83'
                 b'vRRcHKnKL1joJIRoaZzwPGtuhb9S2lx/J7hERZUNrA2q4nOtLk5c86wjV1sJ'
                 b'GtjlcYcapAUuUfnMH7wXHISgS1ttN2qlPxBG/QKCbSIsbpvVVvMfcDlH1eTg'
                 b'LWphSU7VXE2ULtaGqF5Y7aIo7HZ1mso70TLkY2o4ObjY7BkXGMc+iBUOQoDI'
                 b'MtdR0QoisvxZuS6cteUmjzfnakpipcyRxi64ypOThWrp6mscopU7LSkXc00/'
                 b'x+oswvNhotVlzfVpm/pra5kxutQUlgcyABF0ZWeJ/elcIF61rxCMFVyR0VXt'
                 b'iU2SY4aN7T8iWKxdTk7CEgOwrmZS8G+FEedVKhyEGVmWaS3jP13IfekpD+OJ'
                 b'Bpvcrs4QbObctSYd46j2+AIBvuo9LAT90qK9WyE43xfEQaxVLvnhnh1lhjdO'
                 b'O3IkibGu/S7kD16HQG+A84LoqUPQbElYOudo3V5IATU1t9MD3+Pnf5C/BjX/'
                 b'lZ5VLhUxyotSdpOv6bDMVdX5+dMgBVgID0GmhdD7R37TgO9DChyaOLWo06TV'
                 b'LATlFgpqopXHu6VB3AVtZFXf8qiBvWt4fLdHeh7Z7fMlPeqD1XvQXO1ElPRQ'
                 b'UpXhuk1zOZJQq+fr0jAzKyErHIWhBvEi/igHsn6xN2/KVEgGxF0waOBuSIJK'
                 b'1oQe8P6Kz78/XctRKxKuesYUBoiHvFmeX0MSSBH+OwzOvO7PR5vhDZAEaBpq'
                 b'AcX7dCPoIcnV8uMqrKMRYxMPyb74HxY31f8DEqQi/4ppJln3su0dBxmAy7Nj'
                 b'YQnryhKs5UV8SGpi429guOwf0celsqOK2pUrlG09p/xsDtGGZkeVPmLvMUTH'
                 b'ODu9xDX2l9RMoKEagp8oymPwma/gekK8m78qAQzfPYb6iHPXrS2C6Jke09o5'
                 b'J8X2Rqbp23WLa1Y/5QT6KlwMu271Eec+dDvVPnRA4U2jTNo/bZitpKzcK6Yn'
                 b'50rOODdHhhBdXPvQ9SeODWLbWDt2IohtYbB2ZHV5K4qGyc6MBgiV+/t2ZtSb'
                 b'ouG8M2N/EtmrlAi3g8APWptqyhcPwV6lwnfmRhR4NavrQhhJe5X2J97de0H5'
                 b'qwA3SaB9HsuqePHo4dpMrSGo5svl+wMzwiTLBIg5hLAEe3fvzXU88WLcvXcg'
                 b'ce5nHeKbqVLCUBUWA6z6vv2sixsbT2Dy+1mLhunTx3aGoZTbJoV8zUL+rYTb'
                 b'OXOAxMxLYj/rgSSzwzvYAiC1usshQjqIhNV8VDu8HwMUHULCKW6voNrhHcka'
                 b'w79P4O9T2eQVcSIXcaEb5IdUjUN3h/eBRDa0uD4OLRlcejv238+kCdIxJILo'
                 b'T5Jakk4GPfdHY8gF0Z9+mqKOiyAz2AkPQ5TzdQwrQUTjghX84zVnA8YPDXWO'
                 b'j8X/AaJKDv9LHyuuAAAAAElFTkSuQmCC',
                                      'save_btn': b'iVBORw0KGgoAAAANSUhEUgAAAFgAAAAfCAYAAABjyArgAAAACXBIWXMAAAsTAAAL'
             b'EwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJFSURBVHgB7ZrL'
             b'TsJAFIYPXjYmRhcs1CjBnT6BlxU8gySGdzCBhAcw7iXCE7hko89AVyJPgDsJCzWR'
             b'NVvsP9NT2nKR2B6Cer4E2g6n05l//hlmYFLk0dnJ5ihF1+5pjpQ4ODSkm+OProOL'
             b'FN46u9mme8ilKyVS4tOv1nFwjt+7+ZTn3GbmoUEb56ekxGfw9Ey9QpFcJ+dXrza3'
             b'713nZrcuC6Qkw/rBvjkOWu3sCumYK0luhRRRVGBhVGBhVGBhVGBh/qTA/WrNzEWX'
             b'AVGBzYT7okgve4fmhfNFVBwrqUFrOQReIyH81YwLL8FR8X6VKPOPVoxiAnvrcYou'
             b'wY27PBfDZRtnp+ZzpE26ZtKVsr0nEIcj0oOxSB8vS80/n5Y/pyeNnIO5woFCQwwW'
             b'CpWG2OmKjUE8XwO431b6xGuUNmUeG34cUd3Pk3sK4rlhGQxNNq7k33f09hrIh8tG'
             b'v0vgKFEXfQcEGbmtPTamcs/g3oB4djMLHs3HlqMeKgvfJ8XCBAYsFLt0GhDDClGf'
             b'GWPyjAg/yYVBwReN2CyCXTpyWNl093kw0yxXOLgU3fmnv1Pj2WgklCVOPnEQczAq'
             b'0yt4FfRcBgcztgHs2NqnWugzht05y8loOB6jo/kE3W2+1CY8QxoxgdFV4UB0z/Bs'
             b'YDTm8UyAZwWjmLIVzPtS4rhpBJ8zKR+ko7HnGfsTx/27aPh5ezdUkgWaQlv9LUIY'
             b'FVgYFVgYFVgYFVgYFVgYCOyQIoWjO3sECO7s0b1pAoT2pnGi7q5MjNDuyi/2g5fC'
             b'y1z4aAAAAABJRU5ErkJggg=='
                                      }
        self.window = Tk()
        self.window.title("Pybot Debugger v2.2")
        self.window.iconbitmap(f"{current_path}\\functions\\src\\logo_pybot.ico")
        # Create radioButton variable
        self.radio_button_var = IntVar()
        # Seteo de dimensiones en pantalla y cálculos
        # Se toman la resolución de la pantalla desde sistema
        self.user32 = ctypes.windll.user32
        self.screensize = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)
        self.normalized_height = self.screensize[1]  # alto de pantalla
        self.normalized_width = self.screensize[0]  # ancho de pantalla
        self.task_bar_height = 50
        # Calculo el alto de la pantalla restando la dimensión de la task_bar de windows
        self.final_height_for_use = (self.normalized_height - self.task_bar_height)
        # Dimensiones screen base
        self.base_screen_height = 501
        self.base_screen_width = 187
        # Dimensiones screen refab
        self.refab_screen_height = 501
        self.refab_screen_width = 230

        # Centrando en pantalla, pantalla inicial
        self.x_base = (self.normalized_width / 2) - (self.base_screen_height / 2)
        self.y_base = (self.final_height_for_use / 2) - (self.base_screen_width / 2)
        # Centrando en pantalla, pantalla secundaria
        self.x_refab = (self.normalized_width / 2) - (self.refab_screen_height / 2)
        self.y_refab = (self.final_height_for_use / 2) - (self.refab_screen_width / 2)

    def backBtn(self):
        self.fixer()

    def set_radio_btn_status(self, button_status):
        if button_status == 6:
            self.json_GetFieldBy = "Xpath"
        if button_status == 7:
            self.json_GetFieldBy = "Id"
        if button_status == 8:
            self.json_GetFieldBy = "Name"
        return self.json_GetFieldBy

    def get_radio_btn_status(self):
        return self.json_GetFieldBy

    def save_btn(self, incoming_text_input):
        # Flujo lógico de cambio
        # *******************************************************************
        incoming_text_input = incoming_text_input.replace("\n", "")
        # corre la función que se encarga de leer el value del radio button y entrega el value correspondiente
        self.json_strings[self.debug_this_entity]['GetFieldBy'] = self.get_radio_btn_status()
        self.json_strings[self.debug_this_entity]['ValueToFind'] = incoming_text_input
        self.json_GetFieldBy = self.json_strings[self.debug_this_entity]['GetFieldBy']
        self.json_ValueToFind = self.json_strings[self.debug_this_entity]['ValueToFind']
        input_file = open(self.path_json_complete, "w", encoding="utf8")
        self.json_strings = json.dumps(self.json_strings, indent=4, ensure_ascii=False)
        input_file.write(self.json_strings)
        input_file.close()
        self.send_this_code = 1
        self.window.destroy()
        return self.send_this_code, self.json_ValueToFind, self.json_GetFieldBy
        # *******************************************************************

    def refab_window(self):
        # Se setea el default value para los radio buttons
        if self.json_GetFieldBy == "Xpath":
            self.radio_button_var.set(6)
        if self.json_GetFieldBy == "Id":
            self.radio_button_var.set(7)
        if self.json_GetFieldBy == "Name":
            self.radio_button_var.set(8)
        self.window.geometry(f"{self.refab_screen_height}x{self.refab_screen_width}+"
                             f"{int(self.x_refab)}+{int(self.y_refab)}")
        self.window.configure(bg="#ffffff")
        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=230,
            width=501,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)
        # Other labels
        # ************************************************************************************************************
        entity_name_label = tkinter.Label(self.window, text="Nombre del Objeto", bg="white",
                                          fg="black", font=f'{self.unified_font} 10 bold')
        entity_name_label.place(x=14, y=3, width=128, height=42)
        object_label = tkinter.Label(self.window, text=f"{self.debug_this_entity}", bg="white",
                                     fg="#B6040B", font=f'{self.unified_font} 12 bold')
        object_label.place(x=1, y=36, width=256, height=32)
        new_expresion_label = tkinter.Label(self.window, text="Nueva Expresión", bg="white",
                                            fg="black", font=f'{self.unified_font} 10 bold')
        new_expresion_label.place(x=10, y=78, width=128, height=32)
        identifier_type_label = tkinter.Label(self.window, text="Tipo de Identificador", bg="white",
                                              fg="black", font=f'{self.unified_font} 10 bold')
        identifier_type_label.place(x=325, y=6, width=135, height=32)
        # ************************************************************************************************************
        img0 = PhotoImage(data=self.stored_images['save_btn'])
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.save_btn(entity_input_text_box.get("1.0", END)),
            relief="flat")
        b0.place(
            x=151, y=185,
            width=88,
            height=31)

        img1 = PhotoImage(data=self.stored_images['back_btn'])
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.backBtn,
            relief="flat")

        b1.place(
            x=256, y=185,
            width=78,
            height=31)

        entry0_img = PhotoImage(data=self.stored_images['input_text'])
        entry0_bg = canvas.create_image(
            247.0, 144.5,
            image=entry0_img)

        # Text Box Management
        entity_input_text_box = Text(self.window)
        entity_input_text_box.place(x=24, y=115, width=445.0, heigh=53)
        entry_placeholder = tkinter.StringVar()
        entry_placeholder.set(self.json_ValueToFind)
        entity_input_text_box.insert(INSERT, self.json_ValueToFind)

        # Radio buttons create
        self.radio_xpath = Radiobutton(self.window, value=6, variable=self.radio_button_var,
                                       bg="white", fg="#B6040B",
                                       command=lambda:self.set_radio_btn_status(self.radio_button_var.get()))
        self.radio_xpath.place(x=318, y=55, width=32, height=32)
        self.radio_id = Radiobutton(self.window, value=7, variable=self.radio_button_var,
                                    bg="white", fg="#B6040B",
                                    command=lambda: self.set_radio_btn_status(self.radio_button_var.get()))
        self.radio_id.place(x=380, y=55, width=32, height=32)
        self.radio_name = Radiobutton(self.window, value=8, variable=self.radio_button_var,
                                      bg="white", fg="#B6040B",
                                      command=lambda: self.set_radio_btn_status(self.radio_button_var.get()))
        self.radio_name.place(x=440, y=55, width=32, height=32)

        # Radio buttons Labels
        xpath_radio = tkinter.Label(self.window, text="Xpath", bg="white", fg="black",
                                    font=f'{self.unified_font} 8 bold')
        xpath_radio.place(x=318, y=75, width=32, height=32)
        id_radio = tkinter.Label(self.window, text="ID", bg="white", fg="black",
                                 font=f'{self.unified_font} 8 bold')
        id_radio.place(x=380, y=75, width=32, height=32)
        name_radio = tkinter.Label(self.window, text="Name", bg="white", fg="black",
                                   font=f'{self.unified_font} 8 bold')
        name_radio.place(x=440, y=75, width=32, height=32)

        self.window.resizable(False, False)
        self.window.mainloop()
        return self.send_this_code, self.json_ValueToFind, self.json_GetFieldBy

    def btn_retry(self):
        self.send_this_code=1
        self.window.destroy()
        return self.send_this_code, self.json_ValueToFind, self.json_GetFieldBy

    def obtain_project_id(self):
        with open(self.instancia.path_config, 'r') as info:
            yaml_dic = yaml.safe_load(info)
            id_project = (yaml_dic['Project']['ID'])
        return id_project

    def obtain_label_id(self):
        login = os.getlogin()
        label_id = self.instancia.get_data_from_xml_encrypted("TOKEN", "id", login, "LABEL")
        return label_id

    def obtain_true_custom_fields(self):
        with open(self.instancia.path_config, 'r') as info:
            yaml_dic = yaml.safe_load(info)
            true_custom_fields = yaml_dic['Project']['True_Custom_Fields']
            return true_custom_fields

    def obtain_token_ID(self):
        login = os.getlogin()
        token_jira = self.instancia.get_data_from_xml_encrypted("TOKEN", "id", login, "USER_TOKEN")
        return token_jira

    def btn_report(self):
        true_custom_field = self.obtain_true_custom_fields()
        proj_id = self.obtain_project_id()
        lab_id = self.obtain_label_id()
        #Se obtiene el token del informador del reporte
        token_jira= self.obtain_token_ID()
        #Se realiza un screenshot
        image_file = self.instancia.memory_image
        #se tiene que modificar para que lo tome a través de la UI /va la info del resource y data cache
        user_description_text = input("ingrese un texto: ")
        while len(user_description_text) == 0:
            user_description_text = input("ingrese un texto: ")
        jira_obj = Jira.JiraConnections(self.instancia, user_description_text, self.debug_this_entity, proj_id,
                                        image_file, self.instancia.data_cache, self.instancia.data_resource,
                                        self.incomming_exception, lab_id, token_jira, true_custom_field)
        if jira_obj.report_defect == 3312:
            #defecto ya existente
            self.send_this_code = 4
        else:
            self.send_this_code = 3
            self.instancia.tear_down()
            self.window.destroy()
            #al finalizar el reporte, debe cerrar la ejecución
        return self.send_this_code, self.json_ValueToFind, self.json_GetFieldBy

    def openRefabButn(self):
        self.refab_window()

    def fixer(self):
        self.window.geometry(f"{self.base_screen_height}x{self.base_screen_width}+"
                             f"{int(self.x_base)}+{int(self.y_base)}")
        self.window.configure(bg="#ffffff")
        img0 = PhotoImage(data=self.stored_images['save_btn'])

        canvas = Canvas(
            self.window,
            bg="#ffffff",
            height=187,
            width=501,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        canvas.place(x=0, y=0)

        # labels

        error_label = tkinter.Label(self.window, text="Un error inesperado ha ocurrido\n",
                                    bg="white", fg="black", font=f'{self.unified_font} 10 bold')
        error_label.place(x=157, y=1, width=205, height=60)
        label_entity_error = tkinter.Label(self.window, text=f"El objeto {self.debug_this_entity} "
                                                             f"no se visualiza \nen pantalla.",
                                           bg="white", fg="black", font=f'{self.unified_font} 9 bold')
        label_entity_error.place(x=155, y=80, width=300, height=51)
        label_key_exception = tkinter.Label(self.window, text=f"Clave: {self.incomming_exception}", bg="white",
                                            fg="black", font=f'{self.unified_font} 9 bold')
        label_key_exception.place(x=156, y=50, width=190, height=35)
        img0 = PhotoImage(data=self.stored_images['retry_btn'])
        b0 = Button(
            image=img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_retry,
            relief="flat")

        b0.place(
            x=127, y=142,
            width=113,
            height=31)

        img1 = PhotoImage(data=self.stored_images['report_btn'])
        b1 = Button(
            image=img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.btn_report,
            relief="flat")

        b1.place(
            x=375, y=141,
            width=112,
            height=31)

        img2 = PhotoImage(data=self.stored_images['refab_btn'])
        b2 = Button(
            image=img2,
            borderwidth=0,
            highlightthickness=0,
            command=self.openRefabButn,
            relief="flat")

        b2.place(
            x=252, y=142,
            width=112,
            height=31)

        background_img = PhotoImage(data=self.stored_images['sad_face_img'])
        background = canvas.create_image(
            74.0, 78.5,
            image=background_img)

        self.window.resizable(False, False)
        self.window.mainloop()
        return self.send_this_code, self.json_ValueToFind, self.json_GetFieldBy


    def exit_debugger(self):
        self.instancia.tear_down()
        sys.exit()



