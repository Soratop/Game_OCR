import getParameter as gp

print('B級育成')

def main():
    # ボタンの場所などを確認
    gp.getParameter()


    for i in range(500):

        gp.clickRight()

        gp.getSS()

        gp.getText()


main()