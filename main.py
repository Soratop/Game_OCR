import getParameter as gp
import time

print('C級育成')

def main():
    # ボタンの場所などを確認
    gp.getParameter()
    
    for i in range(8):

        gp.clickLeft()

        gp.getSS()

        gp.getText()


main()