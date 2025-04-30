#include <windows.h>

// 窗口类名称和圆形参数
const LPCWSTR CLASS_NAME = L"WatermarkWindow";
const int CIRCLE_RADIUS = 100;
const COLORREF CIRCLE_COLOR = RGB(255, 0, 0); // 红色

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_PAINT: {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(hwnd, &ps);
        RECT rect;
        GetClientRect(hwnd, &rect);

        // 设置透明背景
        SetBkMode(hdc, TRANSPARENT);

        // 绘制红色圆形
        HPEN hPen = CreatePen(PS_SOLID, 3, CIRCLE_COLOR);
        HBRUSH hBrush = CreateSolidBrush(CIRCLE_COLOR);
        SelectObject(hdc, hPen);
        SelectObject(hdc, hBrush);
        Ellipse(hdc, (rect.right - rect.left)/2 - CIRCLE_RADIUS, 
                (rect.bottom - rect.top)/2 - CIRCLE_RADIUS,
                (rect.right - rect.left)/2 + CIRCLE_RADIUS,
                (rect.bottom - rect.top)/2 + CIRCLE_RADIUS);
        DeleteObject(hPen);
        EndPaint(hwnd, &ps);
        return 0;
    }
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    default:
        return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, LPSTR, int nCmdShow) {
    // 注册窗口类
    WNDCLASSW wc = { };
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hbrBackground = (HBRUSH)GetStockObject(BLACK_BRUSH); // 背景透明
    RegisterClassW(&wc);

    // 创建透明窗口
    HWND hwnd = CreateWindowExW(
        WS_EX_LAYERED | WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_TRANSPARENT,
        CLASS_NAME, L"Watermark", WS_POPUP,
        0, 0, 1920, 1080, // 初始窗口大小
        NULL, NULL, hInstance, NULL
    );

    // 设置窗口透明度（0-255，0为完全透明）
    SetLayeredWindowAttributes(hwnd, 0, 50, LWA_ALPHA);

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    // 消息循环
    MSG msg = { };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

