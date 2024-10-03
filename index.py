from Portfolio.api_portfolio  import Portfolio as api_f
import Portfolio.info_portfolio as ipi_f
import pandas as pd

def make_excel_file(pt_list=[186,187,188]):
    li_port = []
    for n in pt_list:
        li_port.append(api_f(n))

    try:
        with pd.ExcelWriter("precios_c.xlsx") as writer:
            for port_n in li_port:
                port_n.df.to_excel(writer, sheet_name=f"{port_n.name}")
    except:
        print("-- Hubo un problema en la creación del archivo... Intente nuevanemte\n")
    else:
        print("-- Se ha creado el documento de manera exitosa.\n")

def principal_route():
    print()
    print("Pozole")
    print()

    make_excel_file()

    all_p = ipi_f.get_all_portfolios_info()

    for key, p in all_p.items():
        print(f"--- {key}")
        print(p.t_price_year_info)
        print()
        print()


if __name__ == "__main__":
    principal_route()
