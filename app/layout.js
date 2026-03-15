export const metadata = { title: "LinguaAI", description: "Yapay Zeka Destekli Dil Öğrenme" };
export default function RootLayout({ children }) {
  return (
    <html lang="tr">
      <body style={{ margin: 0, padding: 0, background: "#09090f" }}>{children}</body>
    </html>
  );
}
