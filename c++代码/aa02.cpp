#include <windows.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    MessageBoxW(
        NULL, 
        L"这是一个消息框示例", 
        L"提示", 
        MB_OK | MB_ICONINFORMATION
    );
    return 0;
}