from pathlib import Path
import subprocess, sys, shutil, json
ROOT=Path(__file__).resolve().parents[1]; INPUT=ROOT/'input'; OUTPUT=ROOT/'output'; WORK=ROOT/'.work'
OUTPUT.mkdir(exist_ok=True); WORK.mkdir(exist_ok=True)
EXT={'.mp4','.mov','.m4v','.webm','.avi','.mkv','.mp3','.wav','.m4a','.aac','.flac','.ogg'}
def run(c): print('$',' '.join(map(str,c)),flush=True); subprocess.run(c,check=True)
def main():
    files=[p for p in INPUT.rglob('*') if p.is_file() and p.suffix.lower() in EXT]
    if not files: raise SystemExit('No media file in input/')
    src=max(files,key=lambda p:p.stat().st_mtime); job=WORK/src.stem; shutil.rmtree(job,ignore_errors=True); job.mkdir(parents=True)
    wav=job/'audio.wav'; run(['ffmpeg','-y','-i',str(src),'-vn','-ac','1','-ar','44100',str(wav)])
    stems=job/'stems'; stems.mkdir()
    target=wav
    try:
        run([sys.executable,'-m','demucs','--two-stems','vocals','-o',str(stems),str(wav)])
        c=list(stems.rglob('no_vocals.wav')); target=c[0] if c else wav
    except Exception as e: print('Demucs fallback:',e)
    md=job/'midi'; md.mkdir(); run([sys.executable,'-m','basic_pitch','--save-midi',str(md),str(target)])
    mids=list(md.glob('*.mid'))+list(md.glob('*.midi')); 
    if not mids: raise RuntimeError('MIDI was not generated')
    out=OUTPUT/src.stem; out.mkdir(exist_ok=True); midi=out/(src.stem+'.mid'); shutil.copy2(mids[0],midi)
    from music21 import converter
    score=converter.parse(str(midi)); xml=out/(src.stem+'.musicxml'); score.write('musicxml',fp=str(xml))
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    pdf=out/(src.stem+'.pdf'); c=canvas.Canvas(str(pdf),pagesize=A4); w,h=A4; c.setFont('Helvetica-Bold',16); c.drawString(40,h-50,'Music to Piano'); y=h-85; c.setFont('Helvetica',9)
    for n in list(score.flatten().notes)[:250]:
        label=str(n.pitch) if hasattr(n,'pitch') else 'Chord '+'.'.join(p.nameWithOctave for p in n.pitches); c.drawString(45,y,label); y-=10
        if y<40: c.showPage(); y=h-40
    c.save(); (out/(src.stem+'.json')).write_text(json.dumps({'source':src.name,'midi':midi.name,'musicxml':xml.name,'pdf':pdf.name},ensure_ascii=False,indent=2),encoding='utf-8')
if __name__=='__main__': main()
