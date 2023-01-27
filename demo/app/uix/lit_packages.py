import importlib


#--- return a list of streamlit packages/pages to render
def packages():
        #--- 
        ary_pkg = []
        ary_pkg.extend(['lit_continentData',
                        'lit_countryData'
                        ])

        ary_pkg.extend(['lit_claimAnalysis',
                        'lit_claimAnomalies'
                        ])
        return ary_pkg

def get_aryPkgDescr():
        #--- load list of pages to display
        aryDescr = []
        aryPkgs = []

        aryModules = packages()
        for modname in aryModules:
                m = importlib.import_module('.'+ modname,'uix')
                aryPkgs.append(m)

                #--- use the module description attribute if it exists 
                #--- otherwise use the module name
                try:
                        aryDescr.append(m.description)
                except:
                        aryDescr.append(modname)
        return [aryDescr, aryPkgs]