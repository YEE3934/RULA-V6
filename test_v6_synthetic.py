import ast, types, numpy as np, cv2, math, time, logging
from pathlib import Path
src=(Path(__file__).resolve().parents[1] / '222.py').read_text()
module=ast.parse(src)
names={'calculate_2d_angle','calculate_3d_angle','_landmark_xy','extract_hand_comparison','draw_hand_overlay','get_wrist_score','get_upper_arm_score','get_lower_arm_score','get_neck_score','get_trunk_score','compute_rula_full','analyze_side_camera'}
subset=ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[])
exec(compile(subset,'<synthetic>','exec'),globals())
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('TABLE_A','TABLE_B','TABLE_C','HAND_CONNECTIONS') for t in n.targets)],type_ignores=[]),'<const>','exec'),globals())
class Pt:
 def __init__(self,x,y,z=0.,vis=0.99): self.x=x;self.y=y;self.z=z;self.visibility=vis
class R:
 def __init__(self,points):
  self.hand_landmarks=[points];self.hand_world_landmarks=[points];self.handedness=[[types.SimpleNamespace(category_name='Right')]]
hands=[Pt(.45,.48),Pt(.47,.48),Pt(.47,.48),Pt(.47,.48),Pt(.47,.48),Pt(.48,.40),Pt(.48,.35),Pt(.48,.32),Pt(.48,.28),Pt(.50,.39),Pt(.50,.35),Pt(.50,.30),Pt(.50,.25),Pt(.52,.40),Pt(.52,.35),Pt(.52,.30),Pt(.52,.25),Pt(.54,.42),Pt(.54,.35),Pt(.54,.30),Pt(.54,.26)]
ret=extract_hand_comparison(R(hands),(1000,1000,3),np.array([450.,480.]),np.array([850.,480.]),np.array([410.,620.]))
assert ret['matched'] and np.isfinite(ret['angle_2d']),ret
ret_bad=extract_hand_comparison(R(hands),(1000,1000,3),np.array([900.,500.]),np.array([450.,480.]),np.array([910.,640.]))
assert not ret_bad['matched'],ret_bad
ret_none=extract_hand_comparison(None,(1000,1000,3),np.array([450.,480.]),None,np.array([410.,620.]))
assert not ret_none['matched']
put_chinese_text=lambda img,*args,**kwargs: img
render=draw_hand_overlay(np.zeros((1000,1000,3),dtype=np.uint8),ret['hand_points'],ret['angle_2d'])
assert render.shape == (1000,1000,3)
# Synthetic RULA reference only checks boundedness and reproducibility of unchanged v5 formulas.
score=compute_rula_full(2,2,1,1,2,2,1,0,0)
assert score[-2] in range(1,8)
# Built hand scoring policy logic uses quality + agreement; independent unit test gate function statement.
assert ret['distance_ratio'] <= .32
print('Synthetic helpers PASS:',ret['angle_2d'],ret['distance_ratio'],ret['hand_world_palm_length'], 'rula',score[-2:])
# Test integrated side analyzer with fake MediaPipe landmarks and Hand result.
class PoseResults:
 def __init__(self, coords):
  self.pose_landmarks=types.SimpleNamespace(landmark=coords)
  self.pose_world_landmarks=types.SimpleNamespace(landmark=coords)
coords=[Pt(.4,.35,0,.99) for _ in range(33)]
for i,x,y in [(11,.32,.3),(12,.48,.3),(13,.34,.42),(14,.46,.42),(15,.34,.54),(16,.45,.54),(17,.35,.61),(18,.51,.61),(19,.37,.61),(20,.47,.61),(21,.33,.56),(22,.45,.56),(23,.32,.65),(24,.48,.65),(25,.33,.8),(26,.47,.8),(27,.33,.95),(28,.47,.95),(7,.32,.2),(8,.49,.2),(2,.45,.18),(5,.35,.18),(0,.46,.18)]:
 coords[i]=Pt(x,y,0,.99)
pose_res=PoseResults(coords)
detect_pose_with_fallback=lambda *_a,**_k:(pose_res,.95,'original')
_visibility_values=lambda r,idx:[.99]*len(idx)
landmarks_meet_visibility=lambda *_a,**_k:True
draw_full_biomechanical_skeleton=lambda img,*a,**k:img.copy()
handpts=[Pt(.45,.54)] + [Pt(.49,.59) for _ in range(20)]
for k,x,y in [(5,.47,.62),(9,.49,.62),(13,.51,.62),(17,.53,.62)]: handpts[k]=Pt(x,y)
class FakeHandTask:
 def detect(self,im):return R(handpts)
class FakeMP:
 class ImageFormat:
  SRGB=1
 class Image:
  def __init__(self,*a,**k): pass
mp=FakeMP()
fm={'is_abducted':False,'is_across_midline':False,'is_out_to_side':False,'is_side_bending':False,'is_neck_side_bending':False}
mods={'leg_score':1,'wrist_twist_score':1,'auto_selection':{}}
a=analyze_side_camera(np.zeros((1000,1000,3),np.uint8),object(),'右手側',fm,0,0,manual_mods=mods,hand_task=None)
b=analyze_side_camera(np.zeros((1000,1000,3),np.uint8),object(),'右手側',fm,0,0,manual_mods=mods,hand_task=FakeHandTask(),hand_scoring_policy='compare')
c=analyze_side_camera(np.zeros((1000,1000,3),np.uint8),object(),'右手側',fm,0,0,manual_mods=mods,hand_task=FakeHandTask(),hand_scoring_policy='gated')
for x in (a,b,c):
 assert x[0],x
 assert '_v6_hand_points' in x[1]
 assert x[1]['右手 Grand Score'] in range(1,8)
assert a[1]['右手 Grand Score']==b[1]['右手 Grand Score']
assert not a[1]['右手Hand匹配成功'] and b[1]['右手Hand匹配成功']
print('Integrated side analyzer mock PASS:',[(x[1]['右手 Grand Score'],x[1]['右手Pose舊版手腕角度'],x[1]['右手PoseHand實驗手腕角度'],x[1]['右手手腕計分演算法']) for x in (a,b,c)])
