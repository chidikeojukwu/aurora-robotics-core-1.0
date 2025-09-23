// two_link_click_ik.cpp
#include <opencv2/opencv.hpp>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>

static const double L1 = 150.0; // pixels
static const double L2 = 110.0; // pixels
static const int    W  = 800, H = 800;

struct Sol { double t1, t2; }; // radians

std::vector<Sol> ik2r(double x, double y){
    std::vector<Sol> out;
    double r2 = x*x + y*y;
    double Rmax = (L1+L2), Rmin = std::fabs(L1-L2);
    if (r2 > Rmax*Rmax + 1e-6 || r2 < Rmin*Rmin - 1e-6) return out;
    double c2 = (r2 - L1*L1 - L2*L2) / (2.0*L1*L2);
    c2 = std::max(-1.0, std::min(1.0, c2));
    double s2p = std::sqrt(std::max(0.0, 1.0 - c2*c2));
    double t2a = std::atan2(s2p,  c2);  // elbow-down
    double t2b = std::atan2(-s2p, c2);  // elbow-up
    auto t1_for = [&](double t2){
        double k1 = L1 + L2*std::cos(t2);
        double k2 = L2*std::sin(t2);
        return std::atan2(y, x) - std::atan2(k2, k1);
    };
    out.push_back({t1_for(t2a), t2a});
    out.push_back({t1_for(t2b), t2b});
    return out;
}

cv::Point2i toPix(double x, double y, const cv::Point2i& C){
    // world: origin at C, y up; image: y down
    return { (int)std::lround(C.x + x), (int)std::lround(C.y - y) };
}

void drawArm(cv::Mat& img, const Sol& s, const cv::Point2i& C, const cv::Scalar& col){
    double x1 = L1*std::cos(s.t1), y1 = L1*std::sin(s.t1);
    double x2 = x1 + L2*std::cos(s.t1 + s.t2);
    double y2 = y1 + L2*std::sin(s.t1 + s.t2);
    cv::Point p0 = C;
    cv::Point p1 = toPix(x1,y1,C);
    cv::Point p2 = toPix(x2,y2,C);
    cv::line(img, p0,p1, col, 5);
    cv::line(img, p1,p2, col, 5);
    cv::circle(img, p0, 6, cv::Scalar(0,0,0), -1);
    cv::circle(img, p1, 6, cv::Scalar(0,0,0), -1);
    cv::circle(img, p2, 6, cv::Scalar(0,0,0), -1);
}

struct State {
    cv::Point2i center{W/2, H/2};
    cv::Point2i target{-1,-1};
    std::vector<Sol> sols;
} S;

void onMouse(int event, int x, int y, int, void*){
    if (event != cv::EVENT_LBUTTONDOWN) return;
    S.target = {x,y};
    // convert to world coords (origin at center, y up)
    double X = x - S.center.x;
    double Y = -(y - S.center.y);
    S.sols = ik2r(X, Y);
}

int main(){
    cv::namedWindow("2-Link IK (click)", cv::WINDOW_AUTOSIZE);
    cv::setMouseCallback("2-Link IK (click)", onMouse);
    double R = L1 + L2;

    while(true){
        cv::Mat img(H, W, CV_8UC3, cv::Scalar(245,245,245));

        // draw reach circles
        cv::circle(img, S.center, (int)std::lround(R), cv::Scalar(220,220,220), 1, cv::LINE_AA);
        cv::circle(img, S.center, (int)std::lround(std::fabs(L1-L2)), cv::Scalar(220,220,220), 1, cv::LINE_AA);

        // axes
        cv::line(img, {S.center.x-350, S.center.y}, {S.center.x+350, S.center.y}, cv::Scalar(220,220,220), 1);
        cv::line(img, {S.center.x, S.center.y-350}, {S.center.x, S.center.y+350}, cv::Scalar(220,220,220), 1);

        // draw solutions if any
        if (!S.sols.empty()){
            drawArm(img, S.sols[0], S.center, cv::Scalar(60,90,200));   // elbow-down (blue-ish)
            drawArm(img, S.sols[1], S.center, cv::Scalar(60,200,120));  // elbow-up (green-ish)

            // info text
            auto deg = [](double r){ return r*180.0/CV_PI; };
            char buf[256];
            std::snprintf(buf, sizeof(buf),
                "Elbow-down:  t1=%.1f deg, t2=%.1f deg  |  Elbow-up: t1=%.1f deg, t2=%.1f deg",
                deg(S.sols[0].t1), deg(S.sols[0].t2), deg(S.sols[1].t1), deg(S.sols[1].t2));
            cv::putText(img, buf, {10, 30}, cv::FONT_HERSHEY_SIMPLEX, 0.65, cv::Scalar(20,20,20), 2);
        }

        // draw target cross
        if (S.target.x >= 0){
            cv::drawMarker(img, S.target, cv::Scalar(0,0,255), cv::MARKER_TILTED_CROSS, 20, 2);
        }

        cv::putText(img, "Click to set target. Press 'q' or ESC to quit.",
                    {10, H-20}, cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(40,40,40), 2);

        cv::imshow("2-Link IK (click)", img);
        int k = cv::waitKey(20);
        if (k == 27 || k == 'q') break;
    }
    return 0;
}
