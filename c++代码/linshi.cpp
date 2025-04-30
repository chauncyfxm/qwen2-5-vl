#include <windows.h>

// 窗口过程函数声明（必须提前声明）
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

// Windows程序入口点
int WINAPI WinMain(HINSTANCE hInst, HINSTANCE, LPSTR, int nCmd) {
    // 初始化窗口类结构体（C++11特性初始化默认值）
    WNDCLASSEX wc{
        sizeof(WNDCLASSEX),   // 结构体大小（必须）
        CS_HREDRAW | CS_VREDRAW, // 窗口重绘标志
        WndProc,             // 消息处理函数指针
        0, 0,                // 类额外内存/窗口额外内存
        hInst,               // 当前实例句柄
        nullptr,             // 图标（简化代码故省略）
        LoadCursor(nullptr, IDC_ARROW), // 默认箭头光标
        nullptr,             // 背景画刷
        nullptr,             // 菜单
        "MinWin",            // 窗口类名
        nullptr              // 小图标
    };
    RegisterClassEx(&wc);    // 注册窗口类

    // 创建窗口核心参数：
    HWND hwnd = CreateWindowEx(
        0,                   // 扩展样式（无）
        "MinWin",            // 注册的类名
        "",                  // 窗口标题（空）
        WS_OVERLAPPEDWINDOW, // 标准窗口样式
        CW_USEDEFAULT, 0,    // X,Y位置（使用默认）
        800, 600,           // 窗口宽高
        nullptr,            // 父窗口
        nullptr,            // 菜单
        hInst,              // 实例句柄
        nullptr             // 创建参数
    );

    // 显示并更新窗口
    ShowWindow(hwnd, nCmd);  // nCmd来自入口参数
    UpdateWindow(hwnd);

    // 消息循环（Windows程序核心）
    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);  // 转换键盘消息
        DispatchMessage(&msg);   // 分发到窗口过程
    }
    return msg.wParam;  // 正确退出代码
}

// 基础窗口过程（直接转发系统默认处理）
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp) {
    return DefWindowProc(hwnd, msg, wp, lp);  // 必须调用默认处理
}