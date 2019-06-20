#include <board.h>
#include <lcd.h>

int main()
{
        board_init();
        lcd_init();

        lcd_puts("Hello World!\n");
        return 0;
}
