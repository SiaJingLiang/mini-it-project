

    print("need get name from global")
    c.execute(f"UPDATE CREDENTIALS set {choice} = {value} WHERE NAME={name}")
    print("Signed up successfully. ")
    conn.commit()