using System;
using DrawPanelLibrary; // ...so we can create DrawingPanels to draw into
using System.Drawing; // ...so we can actually draw (.NET GDI+ graphics)

namespace DrawingStarter
{
    class Program
    {
        //const double Len1 = 90; // everything in mm
        //const double Len2 = 150;
        public static readonly DrawingPanel panel = new DrawingPanel(245, 300);
        public static readonly Bitmap background = new Bitmap(245, 300);
        static void Main(string[] args)
        {
            var graphic = panel.GetGraphics();
            var arm = new Robot(0, panel.Height / 2, 90, 140);

            using (Graphics gr = Graphics.FromImage(background))
            {
                gr.DrawRectangle(Pens.Black, 20, 10, 215, 280);
            }

            graphic.DrawImage(background, new Point(0, 0));
            arm.Show(graphic);
            panel.RefreshDisplay();

            arm.penDown = true;
            //arm.Arm1RunTarget(graphic, 100, 30);
            //arm.Arm2RunTarget(graphic, 100, -30);

            while (true)
            {
                if (panel.Input.ClickAvailable)
                    MoveTo(panel.Input.CurrentMousePos, arm, graphic);
            }

            DrawingPanel.Pause();
        }

        static void MoveTo(Point point, Robot arm, Graphics graphic)
        {
            double distanceSq = (point.X - arm.X) * (point.X - arm.X) + (point.Y - arm.Y) * (point.Y - arm.Y);
            double targetAngle2 = 180 - DegreeFromSides(arm.Len1, arm.Len2, distanceSq);
            double targetAngle1 = - DegreeFromSides(arm.Len1, Math.Sqrt(distanceSq), arm.Len2 * arm.Len2) +
                                  Math.Atan2(point.Y - arm.Y, point.X - arm.X) * 180 / Math.PI;

            arm.Arm1RunTarget(graphic, 100, targetAngle1);
            arm.Arm2RunTarget(graphic, 100, targetAngle2);
        }

        static double DegreeFromSides(double a, double b, double oppSq)
        {
            return Math.Acos((a * a + b * b - oppSq) / (2 * a * b)) * 180 / Math.PI;
        }
    }

    class Robot
    {
        public float X, Y;
        public float Len1, Len2;
        public double Angle1 = 0, Angle2 = 0;
        public bool penDown = false;
        public Robot(double x, double y, double len1, double len2)
        {
            X = (float)x;
            Y = (float)y;
            Len1 = (float)len1;
            Len2 = (float)len2;
        }

        public void Show(Graphics graphic)
        {
            double angle1 = Angle1 * Math.PI / 180;
            double angle2 = Angle2 * Math.PI / 180;
            graphic.FillPie(Brushes.Blue, X - 10, Y - 10, 20, 20, -90, 180);
            var x1 = X + Len1 * (float)Math.Cos(angle1);
            var y1 = Y + Len1 * (float)Math.Sin(angle1);
            graphic.DrawLine(Pens.Blue, X, Y, x1, y1);
            graphic.FillEllipse(Brushes.Blue, x1 - 5, y1 - 5, 10, 10);
            graphic.DrawLine(Pens.Blue, x1, y1, x1 + Len2 * (float)Math.Cos(angle2 + angle1), y1 + Len2 * (float)Math.Sin(angle2 + angle1));
        }

        PointF GetPosition(double a1 = double.NaN, double a2 = double.NaN)
        {
            if (double.IsNaN(a1)) a1 = Angle1;
            if (double.IsNaN(a2)) a2 = Angle2;
            a1 *= Math.PI / 180;
            a2 *= Math.PI / 180;
            return new PointF(X + Len1 * (float)Math.Cos(a1) + Len2 * (float)Math.Cos(a2 + a1),
                              Y + Len1 * (float)Math.Sin(a1) + Len2 * (float)Math.Sin(a2 + a1));
        }

        public void Arm1RunTarget(Graphics graphic, int timePerDegree, double degrees)
        {
            int time = (int)Math.Abs(timePerDegree * (degrees - Angle1));
            double delta = (degrees - Angle1) / time * 100;
            for (int i = 1; i <= time / 100; i++)
            {
                graphic.Clear(Color.White);
                if (penDown)
                {
                    PointF xy = GetPosition();
                    PointF newXY = GetPosition(Angle1 + delta);
                    using (Graphics gr = Graphics.FromImage(Program.background))
                        gr.DrawLine(Pens.Red, xy, newXY);
                }
                Angle1 += delta;
                graphic.DrawImage(Program.background, new Point(0, 0));
                Show(graphic);
                Program.panel.RefreshDisplay();
                System.Threading.Thread.Sleep(100);
            }
            graphic.Clear(Color.White);
            if (penDown)
            {
                PointF xy = GetPosition();
                PointF newXY = GetPosition(degrees);
                using (Graphics gr = Graphics.FromImage(Program.background))
                    gr.DrawLine(Pens.Red, xy, newXY);
            }
            Angle1 = degrees;
            graphic.DrawImage(Program.background, new Point(0, 0));
            Show(graphic);
            Program.panel.RefreshDisplay();
        }

        public void Arm2RunTarget(Graphics graphic, int timePerDegree, double degrees)
        {
            int time = (int)Math.Abs(timePerDegree * (degrees - Angle2));
            double delta = (degrees - Angle2) / time * 100;
            for (int i = 1; i <= time / 100; i++)
            {
                graphic.Clear(Color.White);
                if (penDown)
                {
                    PointF xy = GetPosition();
                    PointF newXY = GetPosition(Angle1, Angle2 + delta);
                    using (Graphics gr = Graphics.FromImage(Program.background))
                        gr.DrawLine(Pens.Red, xy, newXY);
                }
                Angle2 += delta;
                graphic.DrawImage(Program.background, new Point(0, 0));
                Show(graphic);
                Program.panel.RefreshDisplay();
                System.Threading.Thread.Sleep(100);
            }
            graphic.Clear(Color.White);
            if (penDown)
            {
                PointF xy = GetPosition();
                PointF newXY = GetPosition(Angle1, degrees);
                using (Graphics gr = Graphics.FromImage(Program.background))
                    gr.DrawLine(Pens.Red, xy, newXY);
            }
            Angle2 = degrees;
            graphic.DrawImage(Program.background, new Point(0, 0));
            Show(graphic);
            Program.panel.RefreshDisplay();
        }
    }
}
