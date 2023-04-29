class CleaningMap:
    mode: list[str] = ["auto", "manual"]
    duplicates: str = [False, True, "auto"]
    missing_num: str = [False, 'auto', 'linreg', 'knn', 'mean', 'median', 'most_frequent', 'delete'] 
    missing_categ: str = [False, 'auto', 'logreg', 'knn', 'most_frequent', 'delete']
    encode_categ: list = [False, 'auto', ['onehot'], ['label']]
    extract_datetime: str = [False, 'auto', 'D', 'M', 'Y', 'h', 'm', 's']
    outliers: str = [False, "auto", "winz", "delete"]
    outlier_param: int | float = 1.5
    logfile: bool = True
    verbose: bool = False
