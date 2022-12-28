import pytabular as p
import subprocess


def get_msmdsrv() -> list:
    """Runs powershel command to retrieve the ProcessId from Get-CimInstance where Name == 'msmdsrv.exe'.

    Returns:
        list: returns ProcessId(s) in list format to account for multiple PBIX files open at the same time.
    """
    p.logger.debug("Retrieving msmdsrv.exe(s)")
    msmdsrv = subprocess.check_output(
        [
            "powershell",
            """Get-CimInstance -ClassName Win32_Process -Property * -Filter "Name = 'msmdsrv.exe'" | Select-Object -Property ProcessId -ExpandProperty ProcessId""",
        ]
    )
    msmdsrv_id = msmdsrv.decode().strip().splitlines()
    p.logger.debug(f"ProcessId for msmdsrv.exe {msmdsrv_id}")
    return msmdsrv_id


def get_port_number(msmdsrv: str) -> str:
    """Gets the local port number of given msmdsrv ProcessId. Via PowerShell.

    Args:
        msmdsrv (str): A ProcessId returned from `get_msmdsrv()`.

    Returns:
        str: `LocalPort` returned for specific ProcessId.
    """
    port = subprocess.check_output(
        [
            "powershell",
            f"""Get-NetTCPConnection -State Listen -OwningProcess {msmdsrv} | Select-Object -Property LocalPort -First 1 -ExpandProperty LocalPort""",
        ]
    )
    port_number = port.decode().strip()
    p.logger.debug(f"Listening port - {port_number} for msmdsrv.exe - {msmdsrv}")
    return port_number


def get_parent_id(msmdsrv: str) -> str:
    """Gets ParentProcessId via PowerShell from the msmdsrv ProcessId.

    Args:
        msmdsrv (str):  A ProcessId returned from `get_msmdsrv()`.

    Returns:
        str: Returns ParentProcessId in `str` format.
    """
    parent = subprocess.check_output(
        [
            "powershell",
            f"""Get-CimInstance -ClassName Win32_Process -Property * -Filter "ProcessId = {msmdsrv}" | Select-Object -Property ParentProcessId -ExpandProperty ParentProcessId""",
        ]
    )
    parent_id = parent.decode().strip()
    p.logger.debug(f"ProcessId - {parent_id} for parent of msmdsrv.exe - {msmdsrv}")
    return parent_id


def get_parent_title(parent_id: str) -> str:
    """Takes the ParentProcessId and gets the name of the PBIX file.

    Args:
        parent_id (str): Takes ParentProcessId which can be retrieved from `get_parent_id(msmdsrv)`

    Returns:
        str: Returns str of title of PBIX file.
    """
    pbi_title_suffixes: list = [
        " \u002D Power BI Desktop",  # Dash Punctuation - minus hyphen
        " \u2212 Power BI Desktop",  # Math Symbol - minus sign
        " \u2011 Power BI Desktop",  # Dash Punctuation - non-breaking hyphen
        " \u2013 Power BI Desktop",  # Dash Punctuation - en dash
        " \u2014 Power BI Desktop",  # Dash Punctuation - em dash
        " \u2015 Power BI Desktop",  # Dash Punctuation - horizontal bar
    ]
    title = subprocess.check_output(
        ["powershell", f"""(Get-Process -Id {parent_id}).MainWindowTitle"""]
    )
    title_name = title.decode().strip()
    for suffix in pbi_title_suffixes:
        title_name = title_name.replace(suffix, "")
    p.logger.debug(f"Title - {title_name} for {parent_id}")
    return title_name


def create_connection_str(port_number: str) -> str:
    """This takes the port number and adds to connection string. This is pretty bland right now, may improve later.

    Args:
        port_number (str): Port Number retrieved from `get_port_number(msmdsrv)`.

    Returns:
        str: _description_
    """
    connection_str = f"Data Source=localhost:{port_number}"
    p.logger.debug(f"Local Connection Str - {connection_str}")
    return connection_str


def find_local_pbi_instances() -> list:
    """The real genius is from this [Dax Studio PowerBIHelper](https://github.com/DaxStudio/DaxStudio/blob/master/src/DaxStudio.UI/Utils/PowerBIHelper.cs).
    I just wanted it in python not C#, so reverse engineered what DaxStudio did.
    It will run some powershell scripts to pull the appropriate info.
    Then will spit out a list with tuples inside.
    You can use the connection string to connect to your model with pytabular.

    Returns:
        list: Example -  `[('PBI File Name1','localhost:{port}'),('PBI File Name2','localhost:{port}')]`
    """
    instances = get_msmdsrv()
    pbi_instances = []
    for instance in instances:
        p.logger.debug(f"Building connection for {instance}")
        port = get_port_number(instance)
        parent = get_parent_id(instance)
        title = get_parent_title(parent)
        connect_str = create_connection_str(port)
        pbi_instances += [(title, connect_str)]
    return pbi_instances
